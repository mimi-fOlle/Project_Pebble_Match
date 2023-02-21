from django.urls import path

from . import views


urlpatterns = [
path('', views.home, name='home'),
path('index/', views.index, name='index'),
path('about/', views.about, name='about'),
path('account_page/', views.account_page, name='account_page'),
path('quiz_question/', views.quiz_question, name='quiz_question'),
path('match/', views.match, name='match'),
path('logout/', views.logout_view, name='logout'),
]