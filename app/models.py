from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your models here.

QUESTION = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'text {i}',
        'count_answers': i,
        'tags': ['Bootstrap', 'HTML', 'CSS'],
        'reiting': i + 7
    } for i in range(11)
]

QUESTION[10]['tags'] = ['fff']

ANSWERS = [
    {
        'id': i,
        'question_id': 1,
        'content': f'text {i}',
        'reiting': i + 7
    } for i in range(4)
]


class Paginate:
    @staticmethod
    def paginate(objects_list, request, per_page=10):
        paginator = Paginator(objects_list, per_page)

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

        return posts, page, ran


def tags_questions(tag, objects_list):
    if tag[-1] == '/':
        tag = tag[:-1]

    questions_by_teg = []
    for element in objects_list:
        if tag in element['tags']:
            questions_by_teg.append(element)

    return questions_by_teg, tag
