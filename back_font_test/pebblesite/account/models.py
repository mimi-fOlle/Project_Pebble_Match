from django.db import models
from django.db.models import ForeignKey
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    user = ForeignKey(User, on_delete=models.DO_NOTHING)

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=60)
    password = models.CharField(max_length=60)
    remaining_pebble = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    
class Questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    questions = models.CharField(max_length=250)
    a_answer = models.CharField(max_length=100)
    b_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.questions
    
class Results(models.Model):
    results_id = models.AutoField(primary_key=True)
    results_question = models.CharField(max_length=50)

    def __str__(self):
        return self.results_question
    
'''
class Matches(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    user_id_matched = models.ForeignKey(Users, on_delete=models.CASCADE)
    percentage = models.CharField(max_length=40)
    pebble_status = models.EmailField(max_length=50)
    
    def __str__(self):
        return self.pebble_status
'''