from django.shortcuts import redirect, render
from pebblesite import settings
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from account.models import Question, Choice, UserAnswer, Match
from django.db.models import Q, Count
import random


# Create your views here.

# Home Page View
def home(request):
    return render(request, template_name='website/index.html')

def about(request):
    return render(request, template_name='website/about.html')


def register_new_user(form, request):
    existing_user = User.objects.filter(email=form.cleaned_data['email'])

    if existing_user.exists():
        password_reset_url = request.scheme + '://' + request.get_host() + reverse('password_reset')
        existing_user.first().email_user(
            get_template('emails/already_registered_subject.txt').render(context={'site_name': settings.SITE_NAME}),
            get_template('emails/already_registered.html').render(context={'password_reset_url': password_reset_url}))
        raise IntegrityError("Email already exists: %s" % form.cleaned_data['email'])
    else:
        # Create and log in user
        newly_created_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'])
        login(request, newly_created_user)
        

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        try:
            register_new_user(form, self.request)
            messages.success(self.request, 'Thank you for registering. You have been automatically logged in.')
            #return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
            return HttpResponse(get_template('registration/registration_complete.html').render())
            
        except IntegrityError as e:
            print("Error when registering a new user: %s" % e)
            return HttpResponse(get_template('registration/registration_complete.html').render())


@login_required
def view(request):
    return render(request, template_name='account/account.html')


#@transaction.atomic
def quiz(request):
    if request.method == 'POST':
        for question_id in request.POST:
            if question_id.startswith('question'):
                question = Question.objects.get(id=question_id.split('question')[-1])
                choice = Choice.objects.get(id=request.POST[question_id])
                if choice.is_match:
                    user_answer = UserAnswer(user=request.user, question=question, choice=choice, is_match=True)
                else:
                    user_answer = UserAnswer(user=request.user, question=question, choice=choice)
                user_answer.save()

        matches = Match.objects.all()
        user_id = request.user.id
        url = reverse('mymatch', args=[user_id])
        return HttpResponseRedirect(url)
    else:
        questions = Question.objects.all()[:5] # Display 5 questions on a page
        choices = Choice.objects.filter(question=questions[0])[:2] # Each questions with 2 choices
        return render(request, 'website/quiz.html', {'questions': questions, 'choices': choices})
    

def mymatch(request):
    user_answers = UserAnswer.objects.filter(user=request.user)
    total_questions = Question.objects.count()
    match_answers = 0

    for answer in user_answers:
        if answer.choice.is_match:
            match_answers += 1

    percentage = (match_answers / total_questions) * 100
    url = reverse('mymatch', args=[request.user.id])
    return HttpResponseRedirect(url)

#@login_required
def match_result(request, user_id):
    user = User.objects.get(id=user_id)
    user_answers = UserAnswer.objects.filter(user=user)
    total_questions = Question.objects.count()
    match_answers = 0

    for answer in user_answers:
        if answer.choice.is_match:
            match_answers += 1

    percentage = (match_answers / total_questions) * 100

    matches = Match.objects.filter(user1=user) | Match.objects.filter(user2=user)
    matches = list(matches)
    random.shuffle(matches)

    context = {'percentage': percentage, 'matches': matches}
    return render(request, 'website/mymatch.html', context)


def calculate_matches(request):
    user_answers = UserAnswer.objects.values('user').distinct()
    users = User.objects.filter(id__in=user_answers)

    users_list = list(users)
    random.shuffle(users_list)

    matches = []
    for i in range(len(users_list)):
        user1 = users_list[i]
        user1_answers = UserAnswer.objects.filter(user=user1, choice__is_match=True)
        user1_total_questions = UserAnswer.objects.filter(user=user1).count()

        for j in range(i + 1, len(users_list)):
            user2 = users_list[j]
            user2_match_answers = UserAnswer.objects.filter(user=user2, choice__is_match=True)
            user2_total_questions = UserAnswer.objects.filter(user=user2).count()
            common_answers = user1_answers.filter(question__in=user2_match_answers.values_list('question', flat=True))
            common_count = common_answers.count()
            percentage = (common_count / user1_total_questions) * 100
            if percentage > 0:
                match = Match(user1=user1, user2=user2, percentage=percentage)
                matches.append(match)

    Match.objects.bulk_create(matches)
    return HttpResponse('Matches generated successfully!')
