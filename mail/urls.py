from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'send/', views.sendMail, name='sendMail'),
	url(r'forward/(?P<messageID>\d+)', views.forward, name='forward'),
	url(r'reply/(?P<userID>\d+)', views.reply, name='reply'),
	url(r'outbox/', views.outbox, name='outbox'),
	url(r'profile/', views.profile, name='profile'),
	url(r'read/(?P<messageID>\d+)', views.ReadMail, name='read')
]