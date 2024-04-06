from django.db import models

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
