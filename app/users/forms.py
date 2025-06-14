from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=30,
        error_messages={
            "required": "First name is required.",
            "min_length": "First name must be at least 2 characters.",
            "max_length": "First name cannot exceed 30 characters."
        }
    )

    last_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=30,
        error_messages={
            "required": "Last name is required.",
            "min_length": "Last name must be at least 2 characters.",
            "max_length": "Last name cannot exceed 30 characters."
        }
    )

    email = forms.EmailField(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Enter a valid email address."
        }
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
