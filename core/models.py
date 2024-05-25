from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=256)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Board(models.Model):
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField(default=timezone.now)
    is_private = models.BooleanField(default=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_boards')
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
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author_tasks')
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='tg_user')
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f"<TgUser({self.tg_id}, {self.user_id})>"


class Collaborator(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_collaborators')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_collaborators')

    def __str__(self):
        return f"<Collaborator({self.user.id}, {self.board.id})>"
