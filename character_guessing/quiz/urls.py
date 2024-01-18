from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_question/', views.add_question, name='add_question'),
    path('register/', views.register, name='register'),
    path('take_quiz/', views.take_quiz, name='take_quiz'),
    path('quiz_results/', views.quiz_results, name='quiz_results'),
    path('like_question/<int:question_id>/', views.like_question, name='like_question'),
    path('logout/', views.logout_view, name='logout')
]