from django.contrib import admin
from django.urls import path, include
from .views import home, generate_quiz, about, setting
from Gen_Quiz.views import create_quiz, quiz_question, quiz_report, quiz_analysis_view, all_quizzes 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', home, name='home'),
    path('generate_quiz/', generate_quiz, name='generate_quiz'),
    path('about/', about, name='about'),
    path('setting/', setting, name='setting'),
    path('profile/', quiz_analysis_view, name='profile'),
    path('quiz/', create_quiz, name='quiz'),
    path('quiz-question/', quiz_question, name='quiz_question'),
    path('quiz/<int:quiz_id>/report/', quiz_report, name='quiz_report'),
    path('all-quizzes/', all_quizzes, name='all_quizzes')
]
