from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(UserCreationForm):
	email = forms.EmailField(label="이메일")

	class Meta:
		model = User
		fields = ("username", "email")

class ProfileForm(forms.ModelForm):
	
	class Meta:
		model = Profile
		fields = ['avatar', 'bio']