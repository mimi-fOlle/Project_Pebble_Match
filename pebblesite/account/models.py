from django.db import models
from django.db.models import ForeignKey
from django.contrib.auth.models import User


# Create your models here.
class Account(models.Model):
    user = ForeignKey(User, on_delete=models.DO_NOTHING)

class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_text = models.CharField(max_length=250)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    is_match = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
    

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.choice)

    
class Match(models.Model):
    user1 = models.ForeignKey(User, related_name='matches_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='matches_as_user2', on_delete=models.CASCADE)
    user3 = models.ForeignKey(User, related_name='matches_as_user3', on_delete=models.CASCADE, default=1)
    percentage1 = models.FloatField(default=0)
    percentage2 = models.FloatField(default=0)
    percentage3 = models.FloatField(default=0)
    pebble_status = models.IntegerField()
    
    def __str__(self):
        return f"{self.user1.username} matched with {self.user2.username} and {self.user3.username} with a percentages {self.percentage1}%, {self.percentage2}%, {self.percentage3}%"
