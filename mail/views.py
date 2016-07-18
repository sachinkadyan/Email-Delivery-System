from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from . import forms, models
from account import models as AccountModels
def sendMail(request):
	if not request.user.is_authenticated():
		return redirect('login')
	if request.method == 'GET':
		form = forms.SendMailForm()
		template = 'mail/compose.html'
		context = {'form': form}
		return HttpResponse(render(request, template, context))

	form = forms.SendMailForm(request.POST)
	if not form.is_valid():
		template = 'mail/compose.html'
		context = {'form': form}
		return HttpResponse(render(request, template, context))

	recepients = form.cleaned_data['to'].split(', ')
	subject = formself.cleaned_data['subject']
	body = form.cleaned_data['body']
	newmessage = models.Message.objects.create(
			subject=subject,
			body=body,
			sender=request.user,
		)
	newmessage.save()

	for username in recepients:
		recepient = AccountModels.MyUser.objects.get(username=username)
		recepient.messages.add(newmessage)
	template = "mail/message.html"
	context = {'message': "The message has been sent successfully!"}
	return HttpResponse(render(request, template, context))


def ReadMail(request, messageID):
	message = models.Message.objects.get(pk=messageID)
	recepients = message.received_by.all()
	recepient_list = ''
	for recepient in recepients:
		recepient_list += recepient.username + ', '
	template = 'mail/read_mail.html'
	context = {'message': message, 'recepients': recepient_list }
	return HttpResponse(render(request, template, context))


def outbox(request):
	if not request.user.is_authenticated():
		return redirect('login')
	user = request.user
	receivedMessages = models.Message.objects.filter(sender=user).order_by('-timestamp')
	messages_with_recepients = []
	for item in receivedMessages:
		recepients = item.received_by.all()
		message_recepient_pair = {
				'message': item,
				'recepients': recepients
		}
		messages_with_recepients.append(message_recepient_pair)

	template = 'mail/outbox.html'
	context = {'messages': messages_with_recepients}
	return HttpResponse(render(request, template, context))


def profile(request):
	if not request.user.is_authenticated():
		return redirect('login')
	sentMails = models.Message.objects.filter(sender=request.user)
	receivedMails = request.user.messages.all()
	template = 'mail/profile.html'
	context = {
			'sentMailsCount': sentMails.count(),
			'receivedMailsCount': receivedMails.count()
		}
	return HttpResponse(render(request, template, context))


def forward(request, messageID):
	if request.method == 'GET':
		message = models.Message.objects.get(pk=messageID)
		sub_body = {
				'subject': message.subject,
				'body': message.body
		}
		form = forms.SendMailForm(sub_body)
		template = 'mail/compose.html'
		context = {'form': form }
		return HttpResponse(render(request, template, context))

	form = forms.SendMailForm(request.POST)
	if not form.is_valid():
		template = 'mail/compose.html'
		context = {'form': form }
		return HttpResponse(render(request, template, context))

	recepients = form.cleaned_data['to'].split(', ')
	subject = form.cleaned_data['subject']
	body = form.cleaned_data['body']
	sender = request.user
	newmessage = models.Message.objects.create(
			subject=subject,
			body=body,
			sender=sender
		)
	newmessage.save()
	for username in recepients:
		recepient = AccountModels.MyUser.objects.get(username=username)
		recepient.messages.add(newmessage)
	template = "mail/message.html"
	context = {'message': "The message has been forwarded successfully!"}
	return HttpResponse(render(request, template, context))


def reply(request, userID):
	if request.method == 'GET':
		template = 'mail/compose.html'
		recepient = {'to': AccountModels.MyUser.objects.get(pk=userID)}
		form = forms.SendMailForm(recepient)
		context = {'form': form }
		return HttpResponse(render(request, template, context))

	form = forms.SendMailForm(request.POST)
	if not form.is_valid():
		template = 'mail/compose.html'
		context = {'form': form }
		return HttpResponse(render(request, template, context))

	subject = form.cleaned_data['subject']
	body = form.cleaned_data['body']
	sender = request.user
	newmessage = models.Message.objects.create(
			subject=subject,
			body=body,
			sender=sender
		)
	newmessage.save()
	AccountModels.MyUser.objects.get(pk=userID).messages.add(newmessage)
	template = "mail/message.html"
	context = {'message': "The message has been sent successfully!"}
	return HttpResponse(render(request, template, context))
