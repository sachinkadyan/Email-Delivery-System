from django import forms

class SendMailForm(forms.Form):
	to = forms.CharField(max_length=30)
	subject = forms.CharField(max_length=50)
	body = forms.CharField(max_length=255, widget=forms.Textarea)
