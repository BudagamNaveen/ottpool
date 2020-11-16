from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class NewRegistrationForm(UserCreationForm):
	email = forms.EmailField()

	class Meta():
		model = User
		fields =('username','email','password1','password2')

class ProfileUpdateForm(forms.ModelForm):
	class Meta():
		model = Profile
		fields = ['ProfilePic','mobile']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta():
		model = User
		fields = ['username','email']
