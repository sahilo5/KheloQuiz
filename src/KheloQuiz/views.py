from django.shortcuts import render
from Gen_Quiz.models import Quiz


def home(request):
    return render(request, 'layouts/welcome_screen.html')  

def generate_quiz(request):
    return render(request, 'generated_quiz.html')  

def about(request):
    return render(request, 'about.html') 

def setting(request):
    return render(request, 'setting.html')

def profile(request):
    recent_quizzes = Quiz.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'recent_quizzes': recent_quizzes})

    
