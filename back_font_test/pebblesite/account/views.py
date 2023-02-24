from django.shortcuts import get_object_or_404, redirect, render
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
from .models import Question, Choice, UserAnswer, Match
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


#@login_required
def quiz(request):
    questions = Question.objects.all()[:5] # Display 5 questions on a page
    choices = Choice.objects.filter(question=questions[0])[:2] # Each questions with 2 choices
    return render(request, 'website/quiz.html', {'questions': questions, 'choices': choices})



#@login_required
def match_result(request):
    user = request.user
    user_answers = UserAnswer.objects.filter(user=user)
    total_questions = Question.objects.count()
    match_answers = 0

    for answer in user_answers:
        if answer.choice.is_match:
            match_answers += 1

    percentage = (match_answers / total_questions) * 100
    context = {'percentage': percentage}
    return render(request, 'website/mymatch.html', context)

'''
def match_result(request, user_id):
    if request.method == 'POST':
        choices = {}
        user = get_object_or_404(User, id=user_id)
        matches = Match.objects.filter(user=user).order_by('-percentage')
        user_answers = UserAnswer.objects.filter(user=user)
        total_questions = Question.objects.count()
        match_answers = 0

        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                choice_id = int(value)
                choices[question_id] = choice_id

                for answer in user_answers:
                    if answer.choice.is_match:
                        match_answers += 1

                percentage = (match_answers / total_questions) * 100
                context = {'percentage': percentage}
                return render(request, context)

        return redirect('website/mymatch', matches)
'''
            

        

'''
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
                question=question, choice_text_in=matches.choice
            ).count()
            percentage = (num_same_answers / len(users)) * 100
        else:
            percentage = 0
        match_results.append({'question': question, 'percentage': percentage})

    return render(request, 'website/mymatch.html', {'match': match, 'match_results': match_results})
        '''