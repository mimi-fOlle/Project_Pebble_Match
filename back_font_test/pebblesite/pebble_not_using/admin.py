from django.contrib import admin
from .models import User, Question, AnswerOption, Response

# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(Response)
