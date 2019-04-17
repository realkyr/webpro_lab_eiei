from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from polls.models import Poll, Question, Choice, Answer
from .forms import PollForm

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

    if request.method == 'POST':
        for question in question_list:
            name = 'choice ' + str(question.id)
            choice_id = request.POST.get(name)
            if choice_id:
                print(choice_id)
                try:
                    ans = Answer.objects.get(question_id=question.id)
                    ans.choice_id = choice_id
                    ans.save()
                except Answer.DoesNotExist:
                    Answer.objects.create(
                        choice_id=choice_id,
                        question_id=question.id
                    )

    context = {
        'poll_id': poll_id,
        'question_list': question_list,
    }
    return render(request, template_name='detail.html', context=context)


def create(request):
    if request.method == 'POST':
        form = PollForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)

            poll = Poll.objects.create(
                title=form.cleaned_data.get('title'),
                start_date=form.cleaned_data.get('start_date'),
                end_date=form.cleaned_data.get('end_date')
            )
            poll.save()

            for i in range(1, form.cleaned_data.get('no_questions') + 1):
                question = Question.objects.create(
                    text='QQQQ' + str(i),
                    type="01",
                    poll=poll
                )
                question.save()

    else:
        form = PollForm()

    context = {'form': form}
    return render(request, 'create.html', context=context)
