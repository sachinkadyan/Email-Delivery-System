from django import forms
from .models import MyUser

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=30, widget=forms.PasswordInput)


# Can use a ModelForm, but the password field isn't displayed as password field, but as text.
# class SignupForm(forms.ModelForm):
# 	class Meta:
# 		model = MyUser
# 		fields = ['username', 'email', 'first_name', 'last_name', 'dob', 'password']

class SignupForm(forms.Form):
	username = forms.CharField(max_length=30)
	email = forms.EmailField()
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	dob = forms.DateField()
	password = forms.CharField(max_length=30, widget=forms.PasswordInput)