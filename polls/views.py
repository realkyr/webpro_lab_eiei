from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from polls.models import Poll, Question, Choice


# Create your views here.

def index(request):
    poll_list = Poll.objects.annotate(question_count=Count('question'))

    context = {
        'page_title': 'My Polls',
        'poll_list': poll_list
    }

    return render(request, template_name='index.html', context=context)


def detail(request, poll_id):
    question_list = Question.objects.filter(poll_id=poll_id)

    context = {
        'poll_id': poll_id,
        'question_list': question_list,
    }
    return render(request, template_name='detail.html', context=context)
