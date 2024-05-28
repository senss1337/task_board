from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from core.models import Board, Task, Tag, Theme, Column, CustomUser


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'is_private', 'theme']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['text']


class CollaboratorForm(forms.Form):
    username = forms.CharField(label='Username')

    def clean_username(self):
        username = self.cleaned_data['username']
        user = CustomUser.objects.filter(username=username).first()
        if not user:
            raise ValidationError('User does not exist')
        return username


class SubscribeForm(forms.Form):
    tg_id = forms.CharField(max_length=9, required=True, label='Telegram ID')

    def clean_tg_id(self):
        tg_id = self.cleaned_data['tg_id']
        if not tg_id.isdigit() or len(tg_id) != 9:
            raise forms.ValidationError("Введите корректный id")
        return tg_id


class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name', 'description']


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['name', 'color']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    remember_me = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())


class UserEditForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
