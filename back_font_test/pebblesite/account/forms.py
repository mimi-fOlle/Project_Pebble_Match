from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField, PasswordInput, fields
from textwrap import indent
from django.forms.widgets import RadioSelect
from account import models


class RegisterForm(Form):
    username = CharField()
    first_name = CharField()
    last_name = CharField()
    email = EmailField()
    password = CharField(widget=PasswordInput)
    password_confirm = CharField(widget=PasswordInput)

    def clean_password_confirm(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password_confirm'):
            raise ValidationError('Password does not match.')

class QForm(Form):
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
