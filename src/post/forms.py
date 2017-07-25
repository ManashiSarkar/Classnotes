from django import forms
from .models import Post, Message, Settings, Comment
from django.contrib.auth.models import User

class NewPost(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title','content')

class ContactForm(forms.Form):
	name = forms.CharField(max_length=100);
	email = forms.EmailField(max_length=100);
	comment = forms.CharField(max_length=1000,widget=forms.Textarea);

class MessageForm(forms.ModelForm):
	content = forms.CharField(label=(u'Message'),widget=forms.Textarea)
	class Meta:
		model = Message
		fields = ('content',)

class SettingsForm_general(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name','last_name')

class SettingsForm_topics(forms.Form):
	topic = forms.CharField(max_length=100);

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('content',)

		labels = {
			'content' : ("")
		}






