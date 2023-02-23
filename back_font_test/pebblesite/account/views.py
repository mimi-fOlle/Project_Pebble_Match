from django import forms
from django.forms.widgets import RadioSelect
from django.forms import fields, widgets
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
from .models import Question, Choice, Match
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


class QForm(forms.Form):
    q1 = fields.CharField(
        required=True,
        label="1. How do you squeeze your toothpaste?",
        widget=forms.RadioSelect(
            choices=[
                (1, "From the bottom"),
                (2, "I do not care"),
            ]
        ),
        initial=1,
    )
    q2 = fields.CharField(
        required=True,
        label="2. Which one represents you the most?",
        widget=forms.RadioSelect(
            choices=[
                (1, "Sun"),
                (2, "Moon"),
            ]
        ),
        initial=1,
    )
    q3 = fields.CharField(
        required=True,
        label="3. Which way of travel do you prefer?",
        widget=forms.RadioSelect(
            choices=[
                (1, "Cruise ship"),
                (2, "Backpacking"),
            ]
        ),
        initial=1,
    )
    q4 = fields.CharField(
        required=True,
        label="4. What kind of breakfast do you take?",
        widget=forms.RadioSelect(
            choices=[
                (1, "Bacon and eggs"),
                (2, "Pancakes with syrup"),
            ]
        ),
        initial=1,
    )
    q5 = fields.CharField(
        required=True,
        label="5. How do you think about kids?",
        widget=forms.RadioSelect(
            choices=[
                (1, "They are Angels"),
                (2, "They are Devils"),
            ]
        ),
        initial=1,
    )


@login_required
def quiz(request):
    questions = Question.objects.all()
    return render(request, 'account/quiz.html', {'questions': questions})

@login_required
def answer_question(request, question_id):
    question = Question.objects.get(id=question_id)
    selected_choice_id = request.POST['choice']
    selected_choice = Choice.objects.get(id=selected_choice_id)
    selected_choice.votes += 1
    selected_choice.save()

    if question.is_matching_question:
        # Check if there are any other users who have chosen the same answer
        users_with_same_answer = Choice.objects.filter(
            question=question, choice_text=selected_choice.choice_text
        ).exclude(id=selected_choice_id).values_list('user_id', flat=True)

        if users_with_same_answer.exists():
            # Match the current user with one of the other users who have chosen the same answer
            matched_user_id = users_with_same_answer.first()

            # Create a Match object to store the matched users
            match = Match.objects.create(users1=request.user, user2=matched_user_id)
            return redirect('match_result', match_id=match.id)
        
    return redirect('question_list')

@login_required
def match_result(request, match_id):
    matches = Match.objects.get(id=match_id)
    # Calculate the percentage of match results with other users for each question
    questions = Question.objects.exclude(is_matching_question=True)
    match_results = []

    for question in questions:
        # Get all the users who have answered this question
        users = Choice.objects.filter(question=question).values_list('user_id', flat=True)

        # Calculate the percentage of match results with other users
        if len(users) >= 1:
            num_same_answers = Choice.objects.filter(
                question=question, choice_text_in=match.choices
            ).count()
            percentage = (num_same_answers / len(users)) * 100
        else:
            percentage = 0
        match_results.append({'question': question, 'percentage': percentage})

    return render(request, 'account/my_match.html', {'match': match, 'match_results': match_results})
        
