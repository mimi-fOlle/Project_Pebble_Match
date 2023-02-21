from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password1 = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Question(models.Model):
    text = models.CharField(max_length=255)
    answer_a = models.CharField(max_length=255)
    answer_b = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    
class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
    
class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)    

