from . import models
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from .models import Answers, Profiles, Questions, Likequestion, Likeanswers, Tags


# Create your views here.

def index(request):
    posts, page, ran = models.Paginate.paginate(Questions.objects.get_new(), request, 10)
    given = {'questions': models.ProfileGet(posts).get_profile_and_ans, 'user': True, 'page': page, 'range': ran,
             'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())]}
    return render(request, 'index.html', given)


def hot(request):
    posts, page, ran = models.Paginate.paginate(Questions.objects.get_hot(), request, 10)
    given = {'questions': models.ProfileGet(posts).get_profile_and_ans, 'user': True, 'page': page, 'range': ran,
             'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())]}
    return render(request, 'hot.html', given)


def question(request, give_question_id):
    try:
        quest = models.Questions.objects.get(id=give_question_id)
    except Exception as e:
        raise Http404("No Question", e)
    given = {'question': quest, 'answers': models.Answers.objects.filter(question_id=give_question_id),
             'user': False, 'key': models.Gettegs(quest), 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())]}
    return render(request, 'question.html', given)


def login(request):
    user = False
    return render(request, 'login.html', {'user': user, 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
                                          'users': Profiles.objects.all()[:min(6, Profiles.objects.count())]})


def signup(request):
    user = False
    return render(request, 'signup.html', {'user': user, 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
                                           'users': Profiles.objects.all()[:min(6, Profiles.objects.count())]})


def ask(request):
    user = False
    return render(request, 'ask.html', {'user': user, 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
                                        'users': Profiles.objects.all()[:min(6, Profiles.objects.count())]})


def settings(request):
    user = True
    return render(request, 'settings.html', {'user': user, 'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
                                             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())]})


def question_by_teg(request, tag):
    tag = tag[:-1] if tag[-1] == '/' else tag
    posts, page, ran = models.Paginate.paginate(models.Questions.objects.get_tag(tag), request)
    given = {'questions': models.Tagsquestions(posts).answers, 'tag': tag, 'user': False, 'page': page, 'range': ran,
             'tags': Tags.objects.all()[:min(6, Tags.objects.count())],
             'users': Profiles.objects.all()[:min(6, Profiles.objects.count())]}
    return render(request, 'questions_by_teg.html', given)
