from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm  
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm 
from .middlewares import auth, guest
from Gen_Quiz.models import Quiz
# Create your views here.

@guest
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm(initial={'username': '', 'first_name': '', 'last_name': '', 'email': '', 'password1': '', 'password2': ''})
    return render(request, 'registration/register.html', {'form': form})

@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'registration/login.html',{'form':form}) 

@auth
def dashboard_view(request):
    recent_quizzes = Quiz.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'dashboard.html', {'recent_quizzes': recent_quizzes})

def logout_view(request):
    logout(request)
    return redirect('login')
