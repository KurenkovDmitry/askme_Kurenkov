from . import models
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse


# Create your views here.

def index(request):
    user = True

    paginator = Paginator(models.QUESTION, 5)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
        page = 1
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    n = posts.paginator.num_pages

    ran = []

    for i in range(max(1, int(page) - 2), min(n, int(page) + 2) + 1):
        ran.append(i)

    if not (int(n) in ran):
        ran.append('...')
        ran.append(int(n))

    if not (1 in ran):
        ran = [1, '...'] + ran

    given = {'questions': posts, 'user': user, 'page': page, 'range': ran}
    return render(request, 'index.html', given)


def question(request, question_id):
    user = False
    given = {'question': models.QUESTION[question_id], 'answers': models.ANSWERS, 'user': user}
    return render(request, 'question.html', given)


def login(request):
    user = False
    return render(request, 'login.html', {'user': user})


def signup(request):
    user = False
    return render(request, 'signup.html', {'user': user})


def ask(request):
    user = False
    return render(request, 'ask.html', {'user': user})


def settings(request):
    user = True
    return render(request, 'settings.html', {'user': user})


def question_by_teg(request, tag):
    user = False
    if tag[-1] == '/':
        tag = tag[:-1]

    questions_by_teg = []
    for element in models.QUESTION:
        if tag in element['tags']:
            questions_by_teg.append(element)

    paginator = Paginator(questions_by_teg, 5)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
        page = 1
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    n = posts.paginator.num_pages

    ran = []

    for i in range(max(1, int(page) - 2), min(n, int(page) + 2) + 1):
        ran.append(i)

    if not (int(n) in ran):
        ran.append('...')
        ran.append(int(n))

    if not (1 in ran):
        ran = [1, '...'] + ran

    given = {'questions': posts, 'tag': tag, 'user': user, 'page': page, 'range': ran}
    return render(request, 'questions_by_teg.html', given)
