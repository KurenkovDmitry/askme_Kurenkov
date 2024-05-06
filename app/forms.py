from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Questions


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, min_length=4)

    def clean(self):
        super().clean()

        username = self.data.get('username')
        password = self.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Неверный логин или пароль')


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, min_length=4)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')
    email = forms.EmailField()
    name = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли не совпадают')


class SettingsForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    name = forms.CharField(max_length=100)
    avatar = forms.ImageField()

    def c_username(self, initial_username):
        username = self['username'].value()

        print('in_name', initial_username, username)

        # Проверяем, было ли изменено поле username
        if initial_username and initial_username == username:
            # Поле не было изменено, пропускаем проверку
            return True

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует')
        return True

    def clean(self):
        cleaned_data = super().clean()


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(max_length=255, required=False)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if not title:
            raise forms.ValidationError('Название вопроса должно быть заполнено.')

        if not text:
            raise forms.ValidationError('Текст вопроса должен быть заполнен.')

        if Questions.objects.filter(title=title).exists():
            raise forms.ValidationError('Вопрос с таким назваием уже существует')


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, max_length=1000)

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')

        print(text)

        if not text:
            raise forms.ValidationError('Текст ответа должен быть заполнен.')
