from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
#from django.contrib.auth import get_user_model
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

'''
class MatchAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'percentage')

admin.site.register(Match, MatchAdmin)


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email')

    def get_match_results(self, obj):
        matches = Match.objects.filter(user1=obj).order_by('-percentage')
        return [f"{match.user2.username} ({match.percentage}%)"
                for match in matches]
    
    get_match_results.short_description = 'Match Results'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(match_count=account.models.Count('matches'))
        return queryset

    def match_count(self, obj):
        return obj.match_count
    
    match_count.short_description = 'Match Count'

    list_display += ('match_count', 'get_match_results')

admin.site.register(User, UserAdmin)
'''