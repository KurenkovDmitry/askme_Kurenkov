from . import models
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


# Create your views here.

def index(request):
    user = True
    posts, page, ran = models.paginate(models.QUESTION, request)
    given = {'questions': posts, 'user': user, 'page': page, 'range': ran}
    return render(request, 'index.html', given)


def hot(request):
    user = True
    posts, page, ran = models.paginate(models.QUESTION, request)
    given = {'questions': posts, 'user': user, 'page': page, 'range': ran}
    return render(request, 'hot.html', given)


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
    questions_by_teg = models.tags_questions(tag, models.QUESTION)
    posts, page, ran = models.paginate(questions_by_teg, request)
    given = {'questions': posts, 'tag': tag, 'user': user, 'page': page, 'range': ran}
    return render(request, 'questions_by_teg.html', given)
