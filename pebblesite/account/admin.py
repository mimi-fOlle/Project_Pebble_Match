from django.contrib import admin
from .models import User, Question, Choice, UserAnswer, Match

# Register your models here.

#User = get_user_model()
#admin.site.unregister(User)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
