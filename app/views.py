from django.contrib import auth
from . import models
from . import forms
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from .models import Answers, Profiles, Questions, Likequestion, Likeanswers, Tags
from .forms import LoginForm, RegisterForm, SettingsForm, QuestionForm, AnswerForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profiles.objects.filter(user=request.user).first()

    posts, page, ran = models.Paginate.paginate(Questions.objects.get_new(), request, 10)
    given = {'questions': models.ProfileGet(posts).get_profile_and_ans, 'user': request.user, 'page': page, 'range': ran,
             'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
             'profile': profile}
    return render(request, 'index.html', given)


def hot(request):
    profile_av_ur = None
    if request.user.is_authenticated and request.user.profiles.avatar:
        profile_av_ur = request.user.profiles.avatar.url

    posts, page, ran = models.Paginate.paginate(Questions.objects.get_hot(), request, 10)
    given = {'questions': models.ProfileGet(posts).get_profile_and_ans, 'user': request.user, 'page': page, 'range': ran,
             'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
             'profileava': profile_av_ur}
    return render(request, 'hot.html', given)


def question(request, give_question_id):
    profile_av_ur = None
    if request.user.is_authenticated and request.user.profiles.avatar:
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

    if 'username' in request.POST:
        username = request.POST['username']
    else:
        username = ""
    if 'email' in request.POST:
        email = request.POST['email']
    else:
        email = ""
    if 'name' in request.POST:
        name = request.POST['name']
    else:
        name = ""

    return render(request, 'signup.html', {'user': request.user, 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
                                           'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
                                           'form': form, 'usn': username, 'em': email, 'na': name})


def ask(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))

    profile_av_ur = None
    if request.user.is_authenticated and request.user.profiles.avatar:
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
    if request.user.is_authenticated and request.user.profiles.avatar:
        profile_av_ur = request.user.profiles.avatar.url

    tag = tag[:-1] if tag[-1] == '/' else tag
    posts, page, ran = models.Paginate.paginate(models.Questions.objects.get_tag(tag), request)
    given = {'questions': models.Tagsquestions(posts).answers, 'tag': tag, 'user': request.user, 'page': page, 'range': ran,
             'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())],
             'profileava': profile_av_ur}
    return render(request, 'questions_by_teg.html', given)


@login_required
@require_POST
def like_dislike_question(request):
    data = json.loads(request.body)
    question_id = data.get('id')
    action = data.get('type')
    profile = request.user.profiles

    try:
        question = Questions.objects.get(id=question_id)
        like, created = Likequestion.objects.get_or_create(
            question_id=question, profile_id=profile,
            defaults={'marker': action == 'like'}
        )

        if not created:
            if action == 'like' and not like.marker:
                question.rating += 2
                like.marker = True
            elif action == 'dislike' and like.marker:
                question.rating -= 2
                like.marker = False
            else:
                return JsonResponse({'rating': question.rating})
        else:
            if action == 'like':
                question.rating -= 1
            else:
                question.rating += 1

        like.save()
        question.save()
        return JsonResponse({'rating': question.rating})

    except Questions.DoesNotExist:
        return JsonResponse({'error': 'Question does not exist'}, status=404)


@login_required
@require_POST
def like_dislike_answer(request):
    data = json.loads(request.body)
    answer_id = data.get('id')
    action = data.get('type')
    profile = request.user.profiles

    try:
        answer = Answers.objects.get(id=answer_id)
        like, created = Likeanswers.objects.get_or_create(
            answer_id=answer, profile_id=profile,
            defaults={'marker': action == 'like'}
        )

        if not created:
            if action == 'like' and not like.marker:
                answer.rating += 2
                like.marker = True
            elif action == 'dislike' and like.marker:
                answer.rating -= 2
                like.marker = False
            else:
                return JsonResponse({'rating': answer.rating})
        else:
            if action == 'like':
                answer.rating -= 1
            else:
                answer.rating += 1

        like.save()
        answer.save()
        return JsonResponse({'rating': answer.rating})

    except Answers.DoesNotExist:
        return JsonResponse({'error': 'Answer does not exist'}, status=404)


@login_required
@require_POST
def set_correct_answer(request):
    import json
    data = json.loads(request.body)
    answer_id = data.get('answer_id')
    is_checked = data.get('is_checked')

    print(f"Answer ID: {answer_id}, Is Checked: {is_checked}")

    try:
        answer = Answers.objects.get(id=answer_id)
        question = answer.question_id

        print(f"User ID: {request.user.id}, Author ID: {question.profile_id.id}")

        if request.user.id != question.profile_id.id:
            return JsonResponse({'status': 'error', 'message': 'Вы не автор этого вопроса.'})

        # Сброс всех других правильных ответов
        Answers.objects.filter(question_id=question, right=True).update(right=False)

        answer.right = is_checked
        answer.save()

        return JsonResponse({'status': 'success'})
    except Answers.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Ответ не найден.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
