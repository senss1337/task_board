from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
import requests

from core.models import TgUser
from .forms import SubscribeForm

TOKEN = "5360985085:AAEx-eXJ2WHsHXLMZzBPxWhBNbJNU77wKyQ"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"


@login_required
def subscribe_on_events(request):
    """Отображение страницы подписки на уведомления"""
    user = request.user
    tg_user = TgUser.objects.filter(user=user).first()
    is_subscribed = tg_user.is_subscribed if tg_user else False
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            tg_id = form.cleaned_data['tg_id']
            with transaction.atomic():
                if not tg_user:
                    tg_user = TgUser(user=user, tg_id=tg_id, is_subscribed=True)
                else:
                    tg_user.tg_id = tg_id
                    tg_user.is_subscribed = True
                tg_user.save()
                messages.success(request, "Вы успешно добавили/обновили свой аккаунт")
            return redirect('subscribe_on_events')
        else:
            messages.error(request, "Введите корректный id")
    else:
        form = SubscribeForm()

    return render(request, "subscribe_on_events.html", {
        "form": form, "tg_user": tg_user, "is_subscribed": is_subscribed
    })


@login_required
def unsubscribe_from_events(request):
    """Отписываемся от уведомлений бота"""
    user = request.user
    tg_user = TgUser.objects.filter(user=user).first()
    is_subscribed = False

    if not tg_user:
        messages.error(request, "Вы не добавили свой Telegram аккаунт")
    else:
        tg_user.is_subscribed = False
        tg_user.save()
        messages.success(request, "Вы отписались от обновлений")

    return render(request, "subscribe_on_events.html", {
        "tg_user": tg_user,
        "is_subscribed": is_subscribed,
    })


def send_messages(text, tg_user_id):  # pragma: no cover
    """Универсальная функция, которая совершает запрос к телеграм бот API"""
    response = requests.post(
        BASE_URL + "sendMessage", data={"chat_id": tg_user_id, "text": text}
    )
    return response.json()


"""Описание сообщений для различных событий"""


def task_added_message(tg_user_id, board_name, col_name, task_name):  # pragma: no cover
    send_messages(
        f"➕ На доске {board_name} в столбце {col_name} создана новая задача '{task_name}'",
        tg_user_id,
    )


def task_updated_message(tg_user_id, board_name, col_name):  # pragma: no cover
    send_messages(
        f"🔵 На доске {board_name} обновлена задача в столбце {col_name}", tg_user_id
    )


def task_deleted_message(tg_user_id, board_name, col_name):  # pragma: no cover
    send_messages(
        f"❌ На доске {board_name} удалена задача в столбце {col_name}", tg_user_id
    )


def col_added_message(tg_user_id, board_name, col_name):  # pragma: no cover
    send_messages(f"➕ На доске {board_name} добавлен столбец {col_name}", tg_user_id)


def col_deleted_message(tg_user_id, board_name, col_name):  # pragma: no cover
    send_messages(f"❌ На доске {board_name} удален столбец {col_name}", tg_user_id)


def collaborator_added_message(tg_user_id, board_name, user_name):  # pragma: no cover
    send_messages(
        f"➕ На доску {board_name} добавлен новый участник {user_name}", tg_user_id
    )


def collaborator_deleted_message(tg_user_id, board_name, user_name):  # pragma: no cover
    send_messages(f"❌ С доски {board_name} удален участник {user_name}", tg_user_id)


def as_collaborator_added_message(tg_user_id, board_name):  # pragma: no cover
    send_messages(f"➕ Вы были добавлены на доску {board_name}", tg_user_id)


def board_deleted_message(tg_user_id, board_name):  # pragma: no cover
    send_messages(f"❌ Доска {board_name} была удалена", tg_user_id)


def task_moved_message(tg_user_id, board_name, task_name, col_name):  # pragma: no cover
    send_messages(
        f"🔵 На доске {board_name} в колонку {col_name} была перемещена задача {task_name}",
        tg_user_id,
    )


def board_edit_message(tg_user_id, board_name, user_name):  # pragma: no cover
    send_messages(
        f"🔵 Доска {board_name} была изменена пользователем {user_name}",
        tg_user_id,
    )


def column_edit_message(tg_user_id, board_name, col_name, user_name):  # pragma: no cover
    send_messages(
        f"🔵 На доске {board_name} была изменена колонка {col_name} пользователем {user_name}",
        tg_user_id,
    )


def task_deadline_message(tg_user_id, board_name, col_name, task_name):  # pragma: no cover
    send_messages(
        f"🔵 На доске {board_name} в колонке {col_name} завтра наступает дедлайн задачи {task_name}",
        tg_user_id,
    )


def send_notification(tg_users: list, send_message, *params):  # pragma: no cover
    """Отправка уведомлений в телеграм боте"""
    for tg_user in tg_users:
        send_message(tg_user.tg_id, *params)
