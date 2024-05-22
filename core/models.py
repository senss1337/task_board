from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    password = models.CharField(max_length=256)

    def __str__(self):
        return f"<User({self.id}, {self.username})>"


class Board(models.Model):
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField(default=timezone.now)
    is_private = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_boards')
    theme = models.ForeignKey('Theme', on_delete=models.CASCADE, related_name='boards')

    def __str__(self):
        return f"<Board({self.id}, {self.name})>"


class Theme(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return f"<Theme({self.id}, {self.name})>"


class Color(models.Model):
    value = models.CharField(max_length=20)
    description = models.CharField(max_length=15)

    def __str__(self):
        return f"<Color({self.id}, {self.value})>"


class Column(models.Model):
    name = models.CharField(max_length=64)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_columns')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='color_columns')

    def __str__(self):
        return f"<Column({self.id}, {self.name})>"


class Task(models.Model):
    text = models.CharField(max_length=128)
    date_created = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_tasks')
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='column_tasks')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_tasks')
    date_deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"<Task({self.id}, {self.text})>"


class Tag(models.Model):
    text = models.CharField(max_length=15, default="Нет тэга")
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='tag')

    def __str__(self):
        return f"<Tag({self.id}, {self.text})>"


class TgUser(models.Model):
    tg_id = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tg_user')
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f"<TgUser({self.tg_id}, {self.user_id})>"


class Collaborator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_collaborators')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_collaborators')

    def __str__(self):
        return f"<Collaborator({self.user.id}, {self.board.id})>"
