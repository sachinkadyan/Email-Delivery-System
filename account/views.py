from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.core.urlresolvers import reverse

from .import forms, models
# Create your views here.
def login(request):
	if request.user.is_authenticated():
		return redirect(reverse('home'))

	if request.method == 'GET':
		form = forms.LoginForm()
		template = 'account/login.html'
		context = {'form': form}
		return HttpResponse(render(request, template, context))

	form = forms.LoginForm(request.POST)
	if not form.is_valid():
		context = {'form': form}
		return HttpResponse(render(request, template, context))

	username = form.cleaned_data['username']
	password = form.cleaned_data['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			user_login(request, user)
			print(user.first_name, user.last_name)
			return redirect(reverse('home'))

	else:
		template = "mail/message.html"
		context = {'message': "The username or password is incorrect!"}
		return HttpResponse(render(request, template, context))



def home(request):
	if not request.user.is_authenticated():
		return redirect('login')
	print(request.user.first_name)
	messages = request.user.messages.all().order_by('-timestamp')
	print messages
	template = 'account/home.html'
	context = {'messages':messages}
	return HttpResponse(render(request, template, context))


def signup(request):
	if request.method == 'GET':
		form = forms.SignupForm()
		template = 'account/signup.html'
		context = {'form': form}
		return HttpResponse(render(request, template, context))

	user = request.POST
	form = forms.SignupForm(user)
	template = 'account/signup.html'
	if not form.is_valid():
		context = {'form': form}
		return HttpResponse(render(request, template, context))

	username = form.cleaned_data['username']
	password = form.cleaned_data['password']
	email = form.cleaned_data['email']
	first_name = form.cleaned_data['first_name']
	last_name = form.cleaned_data['last_name']
	dob = form.cleaned_data['dob']

	newuser = models.MyUser.objects.create(
		username=username, 
		password=password, 
		email=email, 
		first_name=first_name, 
		last_name=last_name, 
		dob=dob
		)
	newuser.set_password(password)
	newuser.save()

	template = "mail/message.html"
	context = {'message': "Congrats! Your account has been successfully created."}
	return HttpResponse(render(request, template, context))


def logout(request):
	user_logout(request)
	return redirect(reverse('login'))