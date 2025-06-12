from django.shortcuts import render
from Gen_Quiz.models import Quiz,UserResponse
from django.db.models import Avg


def home(request):
    return render(request, 'layouts/welcome_screen.html')  

def generate_quiz(request):
    return render(request, 'generated_quiz.html')  

def about(request):
    return render(request, 'about.html') 

def setting(request):
    return render(request, 'setting.html')