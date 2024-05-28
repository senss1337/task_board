from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, UpdateView
from core.models import Board, Collaborator, Color, Column, Task, Tag, TgUser, User, Theme
from task_tracker.bot import send_notification, task_added_message, task_updated_message, as_collaborator_added_message, \
    collaborator_deleted_message
from task_tracker.forms import BoardForm, TaskForm, CollaboratorForm, ThemeForm, ColumnForm
from datetime import datetime


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        boards = Board.objects.filter(is_private=False) | Board.objects.filter(author=self.request.user)
        context['boards'] = boards
        return context


class MyBoardsView(LoginRequiredMixin, ListView):
    template_name = 'my_boards.html'
    context_object_name = 'boards'

    def get_queryset(self):
        user = self.request.user
        boards = Board.objects.filter(author_id=user.id)
        collaborator_boards = Collaborator.objects.filter(user_id=user.id)
        for collab in collaborator_boards:
            boards.append(collab.board)
        return boards


class AddBoardView(LoginRequiredMixin, CreateView):
    template_name = 'add_board.html'
    form_class = BoardForm
    success_url = reverse_lazy('my_boards')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BoardDetailView(LoginRequiredMixin, DetailView):
    model = Board
    template_name = "view_board.html"
    context_object_name = "board"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_delete'] = self.object.author == self.request.user or self.request.user in [collab.user for collab
                                                                                                 in
                                                                                                 self.object.board_collaborators.all()]
        context['colors'] = Color.objects.all()
        return context


class BoardDeleteView(LoginRequiredMixin, DeleteView):
    model = Board
    success_url = reverse_lazy('my_boards')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return HttpResponse("You don't have permission to delete this board.")
        collaborators = self.object.collaborators.all()
        tg_users = [collaborator.user.tg_user for collaborator in collaborators]
        send_notification(tg_users, f"Board '{self.object.name}' has been deleted.")
        self.object.delete()
        return redirect(self.get_success_url())


class ColumnCreateView(LoginRequiredMixin, CreateView):
    model = Column
    fields = ['name']
    template_name = 'add_column.html'

    def form_valid(self, form):
        board_id = self.kwargs['id']
        board = get_object_or_404(Board, id=board_id)
        if board.author != self.request.user:
            return HttpResponse("You don't have permission to add columns to this board.")
        form.instance.board = board
        response = super().form_valid(form)
        tg_users = [collaborator.user.tg_user for collaborator in board.collaborators.all()]
        send_notification(tg_users, f"Column '{form.instance.name}' has been added to the board '{board.name}'.")
        return response

    def get_success_url(self):
        return reverse_lazy('view_board', kwargs={'id': self.kwargs['id']})


class DeleteColumnView(LoginRequiredMixin, DeleteView):
    model = Column
    success_url = reverse_lazy('my_boards')
    template_name = 'confirm_delete_column.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        board_id = self.object.board_id

        if self.object.board.author != self.request.user and self.request.user not in self.object.board.collaborators.all():
            return HttpResponseForbidden("You don't have permission to delete this column.")

        self.object.delete()

        tg_users = [collaborator.user.tg_user for collaborator in Collaborator.objects.filter(board=self.object.board)]
        send_notification(tg_users,
                          f"Column '{self.object.name}' has been deleted from the board '{self.object.board.name}'.")

        return redirect(self.get_success_url())


class AddTaskView(LoginRequiredMixin, CreateView):
    template_name = 'add_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('my_boards')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.board_id = self.kwargs['board_id']
        form.instance.column_id = self.kwargs['column_id']
        response = super().form_valid(form)
        # Отправка уведомления
        tg_users = [collaborator.user.tg_user for collaborator in
                    Collaborator.objects.filter(board_id=self.kwargs['board_id'])]
        send_notification(tg_users, task_added_message, form.instance.board.name, form.instance.column.name,
                          form.instance.text)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board_id'] = self.kwargs['board_id']
        context['column_id'] = self.kwargs['column_id']
        return context


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('my_boards')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        can_delete = self.object.board.author.id == request.user.id or Collaborator.objects.filter(
            board=self.object.board, user=request.user).exists()
        if not can_delete:
            return HttpResponseForbidden("You don't have permission to delete this task.")
        success_url = self.get_success_url()
        task_name = self.object.text
        self.object.delete()
        tg_users = [collaborator.user.tg_user for collaborator in self.object.board.collaborators.all()]
        send_notification(tg_users, f"Task '{task_name}' has been deleted from the board '{self.object.board.name}'.")
        return HttpResponseRedirect(success_url)


class EditTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'edit_task.html'
    success_url = reverse_lazy('my_boards')

    def form_valid(self, form):
        task = form.save(commit=False)
        tag_text = self.request.POST.get('tag', 'No tag')
        deadline = self.request.POST.get('deadline')
        if tag_text != "No tag":
            tag, created = Tag.objects.get_or_create(task=task)
            tag.text = tag_text
            tag.save()
        if deadline:
            task.date_deadline = datetime.strptime(deadline, "%Y-%m-%d")
        else:
            task.date_deadline = None
        task.save()
        tg_users = [collaborator.user.tg_user.tg_id for collaborator in task.board.collaborators.all()]
        send_notification(tg_users, task_updated_message, task.board.name, task.column.name)
        return super().form_valid(form)

    def get_queryset(self):
        return Task.objects.filter(board__author=self.request.user) | Task.objects.filter(
            board__collaborators__user=self.request.user)


class AddCollaboratorView(LoginRequiredMixin, CreateView):
    model = Collaborator
    form_class = CollaboratorForm
    template_name = 'add_collaborator.html'
    success_url = reverse_lazy('my_boards')

    def form_valid(self, form):
        board_id = self.kwargs['board_id']
        board = Board.objects.get(id=board_id)
        if board.author != self.request.user:
            return super().form_invalid(form)
        new_collaborator = form.save(commit=False)
        new_collaborator.board = board
        new_collaborator.user = User.objects.get(username=form.cleaned_data['username'])
        new_collaborator.save()
        tg_user = TgUser.objects.filter(user_id=new_collaborator.user.id).first()
        if tg_user:
            as_collaborator_added_message(tg_user.tg_id, board.name)
        return super().form_valid(form)


class DeleteCollaboratorView(LoginRequiredMixin, DeleteView):
    model = Collaborator
    template_name = 'delete_collaborator.html'
    success_url = reverse_lazy('my_boards')

    def get(self, request, *args, **kwargs):
        board_id = self.kwargs['board_id']
        collaborator_id = self.kwargs['collaborator_id']
        board = Board.objects.get(id=board_id)
        if board.author != request.user:
            return HttpResponse("You don't have permission to delete collaborators from this board.")
        collaborator = Collaborator.objects.filter(user_id=collaborator_id, board_id=board_id).first()
        if not collaborator:
            return HttpResponseForbidden("Such user does not exist on this board.")
        tg_users = [collaborator.user.tg_user.tg_id for collaborator in board.collaborators.all()]
        for tg_id in tg_users:
            collaborator_deleted_message(tg_id, board.name, collaborator.user.username)
        collaborator.delete()
        return super().get(request, *args, **kwargs)


class FindBoardView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            name = request.POST.get("name")
            board = Board.objects.filter(name=name, is_private=True) | Board.objects.filter(name=name,
                                                                                            author=request.user).first()
            if board:
                answer = {"result": f"<a href='/board/{board.id}'> Найденная доска </a>"}
            else:
                answer = {"result": "Такой доски нет"}
            return JsonResponse(answer)
        else:
            return JsonResponse({"error": "Invalid request"})


class ViewThemesView(LoginRequiredMixin, ListView):
    model = Theme
    template_name = "view_themes.html"
    context_object_name = "themes"


class AddThemeView(LoginRequiredMixin, CreateView):
    template_name = 'add_theme.html'
    form_class = ThemeForm
    success_url = reverse_lazy('view_themes')

    def form_valid(self, form):
        theme_name = form.cleaned_data['name']
        theme_description = form.cleaned_data['description']
        if Theme.objects.filter(name=theme_name).exists():
            messages.error(self.request, "Такая тема уже существует")
            return super().form_invalid(form)
        else:
            messages.success(self.request, "Тема успешно создана")
            return super().form_valid(form)


class EditThemeView(LoginRequiredMixin, UpdateView):
    model = Theme
    template_name = 'edit_theme.html'
    form_class = ThemeForm
    success_url = reverse_lazy('view_themes')

    def form_valid(self, form):
        messages.success(self.request, "Тема успешно отредактирована")
        return super().form_valid(form)


class EditBoardView(LoginRequiredMixin, UpdateView):
    model = Board
    template_name = 'edit_board.html'
    form_class = BoardForm

    def get_success_url(self):
        return reverse_lazy('view_board', kwargs={'id': self.object.id})

    def form_valid(self, form):
        messages.success(self.request, "Доска успешно отредактирована")
        return super().form_valid(form)


class EditColumnView(LoginRequiredMixin, UpdateView):
    model = Column
    template_name = 'edit_column.html'
    form_class = ColumnForm

    def get_success_url(self):
        return reverse_lazy('view_board', kwargs={'id': self.object.board_id})

    def form_valid(self, form):
        messages.success(self.request, "Колонка успешно отредактирована")
        return super().form_valid(form)


def change_task_column(task_id, col_id_new):
    """Изменение колонки у задачи для перетаскивания задач с помощью мыши"""
    task = Task.objects.get(id=task_id)
    task.column_id = col_id_new
    task.save()


class TaskConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = text_data.split()
        task_id = int(data[0].split("-")[-1])
        col_id = int(data[1].split("-")[-1])

        change_task_column(task_id, col_id)

        await self.send(text_data="Task column updated successfully.")


def delete_test_users(request):
    """Удаление тестовых пользователей"""
    users = User.objects.filter(username__in=["TestUser1", "TestUser2", "TestUser3"])
    theme = Theme.objects.filter(name="TestTheme1").first()

    if theme:
        theme.delete()
    if not users:
        return HttpResponse("No users")

    for user in users:
        user.delete()

    return HttpResponse("OK")
