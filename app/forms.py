"""
Definition of forms.
"""

from email import message
from mimetypes import init
from multiprocessing import pool
from random import choice
from tkinter import Widget
from tkinter.tix import Form
from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from django.db import models
from .models import Comment
from .models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

 
    
class PoolAnketaForm(forms.Form):
     name = forms.CharField(label = 'Имя', min_length= 2, max_length= 100)
     mail=  forms.EmailField(label = 'Почта', min_length= 7)
     gender = forms.ChoiceField(label='Пол', choices= [('1','Мужской'), ('2','Женский')], widget=forms.RadioSelect, initial= 1)
     account= forms.BooleanField(label = 'Есть ли у вас аккаунт на сайте?', required= False)
     poolsite = forms.ChoiceField(label= 'На сколько бы вы оценили наш сайт?', choices=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5')),initial= 5)
     message = forms.CharField(label = 'Оставьте комментарий', widget=forms.Textarea(attrs={'rows':12,'cols':20}))

class CommentForm (forms.ModelForm):
      class Meta:
         model = Comment # используемая модель
         fields = ('text',) # требуется заполнить только поле text
         labels = {'text': "Комментарий"} # метка к полю формы text 


class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog 
        fields = ('title','description','content','image',)
        labels = {'title': "Заголовок",'desctiption': "Краткое содержание",'content': "Полное содержание",'image': "Картинка"}
        



