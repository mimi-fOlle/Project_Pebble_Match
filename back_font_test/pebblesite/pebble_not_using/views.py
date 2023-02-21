from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import Question, AnswerOption

def home(request):
    return render(request, 'pebble/home.html')

def index(request):
    return render(request, 'pebble/index.html')

def about(request):
    return render(request, 'pebble/about.html')

# Create your views here.
@login_required
def account_page(request):
    user = request.user
    username = user.username
    return render(request, 'pebble/account_page.html', {'username': username})

@login_required
def quiz(request):
    if request.method == 'POST':
        current_question = int(request.POST.get('current_question'))
        answer_id = int(request.POST.get('answer'))

        question = Question.objects.get(pk=current_question)

        answer = AnswerOption.objects.get(pk=answer_id)

        # Add the answer to the user's session data
        request.session['answers'][current_question] = answer_id

        # If this is the last question, redirect to the match page
        if current_question == Question.objects.count():
            return redirect('match')
        else:
            # Otherwise, go to the next question
            next_question = current_question + 1
            return redirect('quiz_question', question_id=next_question)
        
    else:
        # If this is the first question, initialise the session data
        if 'answer' not in request.session:
            request.session['answers'] = {}

        # Get the first question object from the database
        question = Question.objects.first()

        return redirect('quiz_question', question_id=question.id)
    
@login_required
def quiz_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, 'pebble/quiz_question.html', {'question': question})



def match(request):
    # Get the user's answers from the session data
    answers = request.session.get('answers', {})
    answer_ids = list(answers.values())

    # Get the set of all questions that the user answered
    answered_questions = Question.objects.filter(answer__in=answer_ids)

    # Get the set of all questions that the users did not answer
    unanswered_questions = Question.objects.exclude(answer__in=answer_ids)

    # Calculate the number of matching questions
    num_matching_questions = answered_questions.count()

    # Calculate the percentage of matching questions
    total_questions = Question.objects.count()
    percent_matching = int(num_matching_questions / total_questions * 100)

    # Render the match page with the matching percentage
    return render(request, 'pebble/match.html', {'percent_matching': percent_matching})


def logout_view(request):
    logout(request)
    return redirect('home')