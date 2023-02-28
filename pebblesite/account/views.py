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
import time
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
    

def match_result(request, user_id):
    user = User.objects.get(id=user_id)
    matches = Match.objects.exclude(user1=user).exclude(user2=user).exclude(user3=user).order_by('?')
    unique_matches = set()
    for match in matches:
        if len(unique_matches) >= 1: # 3 results == 1
            break
        match_tuple = (match.user1, match.user2, match.user3)
        if match_tuple not in unique_matches:
            unique_matches.add(match_tuple)
    matches = [Match.objects.get(user1=user1, user2=user2, user3=user3) for (user1, user2, user3) in unique_matches]
    random.seed(time.time())
    random.shuffle(matches)


    context = {'matches': matches}
    return render(request, 'website/mymatch.html', context)
    