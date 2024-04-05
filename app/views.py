from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    questions = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'text {i}'
        } for i in range(10)
    ]
    return render(request, 'index.html', {'questions': questions})
