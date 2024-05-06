from django.contrib import auth
from . import models
from . import forms
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from .models import Answers, Profiles, Questions, Likequestion, Likeanswers, Tags
from .forms import LoginForm, RegisterForm, SettingsForm, QuestionForm, AnswerForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.urls import reverse


# Create your views here.

def index(request):
    profile_av_ur = None
    if request.user.is_authenticated:
        profile_av_ur = request.user.profiles.avatar.url

    posts, page, ran = models.Paginate.paginate(Questions.objects.get_new(), request, 10)
    given = {'questions': models.ProfileGet(posts).get_profile_and_ans, 'user': request.user, 'page': page, 'range': ran,
             'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
             'profileava': profile_av_ur}
    return render(request, 'index.html', given)


def hot(request):
    profile_av_ur = None
    if request.user.is_authenticated:
        profile_av_ur = request.user.profiles.avatar.url

    posts, page, ran = models.Paginate.paginate(Questions.objects.get_hot(), request, 10)
    given = {'questions': models.ProfileGet(posts).get_profile_and_ans, 'user': request.user, 'page': page, 'range': ran,
             'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
             'profileava': profile_av_ur}
    return render(request, 'hot.html', given)


def question(request, give_question_id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    profile_av_ur = None
    if request.user.is_authenticated:
        profile_av_ur = request.user.profiles.avatar.url

    try:
        quest = models.Questions.objects.get(id=give_question_id)
    except Exception as e:
        raise Http404("No Question", e)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']

            # Создаем новый ответ
            answer = Answers.objects.create(answer=text, profile_id=request.user.profiles,
                                              question_id=quest)

            # Перенаправляем пользователя на страницу с вопросами
            return redirect('question', give_question_id=give_question_id)
    else:
        form = QuestionForm(initial={'text': ''})

    given = {'question': quest, 'answers': models.Answers.objects.filter(question_id=give_question_id),
             'user': request.user, 'key': models.Gettegs(quest), 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
             'profileava': profile_av_ur, 'form': form}

    return render(request, 'question.html', given)


def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    login_form = LoginForm()

    login_form.initial['username'] = ""

    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            login_form.initial['username'] = ""
            if user:
                auth.login(request, user)

                # Проверяем, есть ли параметр continue в запросе
                continue_url = request.GET.get('continue')
                if continue_url:
                    return redirect(continue_url)
                else:
                    return redirect(reverse('index'))
        else:
            login_form.initial['username'] = request.POST.get('username', '')

    return render(request, 'login.html', {'user': request.user, 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
                                          'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
                                          'login_form': login_form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Создаем нового пользователя
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            user = User.objects.create_user(username=username, email=email, password=password)

            # Создаем профиль пользователя
            profile = Profiles.objects.create(user=user, name=name)

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
                profile.save()

            # Вход пользователя после успешной регистрации
            auth.login(request, user)
            return redirect('index')  # Замените 'index' на ваше имя маршрута
    else:
        form = RegisterForm()

    # Заполнение формы данными, если они были отправлены, иначе оставить форму пустой
    initial_data = {}
    if 'username' in request.POST:
        initial_data['username'] = request.POST['username']
    else:
        initial_data['username'] = ""
    if 'email' in request.POST:
        initial_data['email'] = request.POST['email']
    else:
        initial_data['email'] = ""
    if 'name' in request.POST:
        initial_data['name'] = request.POST['name']
    else:
        initial_data['name'] = ""

    form = RegisterForm(initial=initial_data)

    return render(request, 'signup.html', {'user': request.user, 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
                                           'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
                                           'form': form})


def ask(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    profile_av_ur = None
    if request.user.is_authenticated:
        profile_av_ur = request.user.profiles.avatar.url

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            tag_names = form.cleaned_data['tags'].split(',')

            # Создаем новый вопрос
            question = Questions.objects.create(title=title, question=text, profile_id=request.user.profiles)

            # Добавляем теги к вопросу
            for tag_name in tag_names:
                tag, _ = Tags.objects.get_or_create(tag=tag_name.strip())
                question.tag_id.add(tag)

            question.save()

            # Перенаправляем пользователя на страницу с вопросами
            return redirect('question', give_question_id=question.id)
    else:
        form = QuestionForm(initial={'title': '', 'text': '', 'tags': ''})

    return render(request, 'ask.html', {'user': request.user, 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
                                        'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
                                        'form': form, 'profileava': profile_av_ur})


def settings(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    profile_ava = None

    initial_data = {
        'username': request.user.username,
        'email': request.user.email,
        'name': request.user.profiles.name if hasattr(request.user, 'profiles') else '',
    }

    if request.method == 'POST':
        last = request.user.username
        form = SettingsForm(request.POST, request.FILES, initial=initial_data)
        if form.c_username(last):
            # Получение данных из формы
            username = form['username'].value()
            email = form['email'].value()
            name = form['name'].value()
            avatar = form['avatar'].value()

            # Обновление данных пользователя
            user = request.user
            if username:
                user.username = username
                user.save()
            if email:
                user.email = email
                user.save()

            # Получение профиля пользователя или создание нового, если он еще не существует
            profile, created = Profiles.objects.get_or_create(user=request.user)

            # Обновление данных профиля
            if name:
                profile.name = name
            if avatar:
                profile.avatar = avatar
            profile.save()

            profile_ava = profile.avatar

            # Перенаправление на страницу настроек после сохранения
            return redirect('settings')  # Замените 'settings' на ваше имя маршрута
    else:
        # Если запрос не POST, создаем форму с данными текущего пользователя
        form = SettingsForm(initial=initial_data)

    return render(request, 'settings.html', {'user': request.user, 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
                                             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
                                             'form': form, 'profileava': request.user.profiles.avatar})


def question_by_teg(request, tag):
    profile_av_ur = None
    if request.user.is_authenticated:
        profile_av_ur = request.user.profiles.avatar.url

    tag = tag[:-1] if tag[-1] == '/' else tag
    posts, page, ran = models.Paginate.paginate(models.Questions.objects.get_tag(tag), request)
    given = {'questions': models.Tagsquestions(posts).answers, 'tag': tag, 'user': request.user, 'page': page, 'range': ran,
             'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
             'profileava': profile_av_ur}
    return render(request, 'questions_by_teg.html', given)
