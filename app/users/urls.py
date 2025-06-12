from django.urls import path 
from . import views
from Gen_Quiz.views import create_quiz


urlpatterns = [
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path("create-quiz/", create_quiz, name="create_quiz"),
]