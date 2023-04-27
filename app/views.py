"""
Definition of views.
"""

from datetime import date, datetime
from email.policy import HTTP
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import PoolAnketaForm
from django.contrib.auth.forms import UserCreationForm

from django.db import models
from .models import Blog

from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария
from .forms import BlogForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Ваши контакты.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'О нас.',
            'year':datetime.now().year,
        }
    )
def pool(request):
    """Renders the pool page."""
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1':'Мужской', '2': 'Женский'}
    poolsite = {'1':'1','2':'2','3':'3','4':'4','5':'5'}
    if request.method == 'POST':
       form = PoolAnketaForm(request.POST)
       if form.is_valid():
           data = dict()
           data['name'] = form.cleaned_data['name']
           data['mail'] = form.cleaned_data['mail']
           data['gender'] = gender[form.cleaned_data['gender']]
           data['message'] = form.cleaned_data['message']
           data['poolsite'] = poolsite[form.cleaned_data['poolsite']]
           if(form.cleaned_data['account'] == True):
               data['account'] = 'Да'
           else:
               data['account'] = 'Нет'
           form = None 
    else:
        form = PoolAnketaForm()

    return render(
        request,
        'app/pool.html',
        {
            'form': form,
            'data': data
        }
    )

def registration(request):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        regform = UserCreationForm (request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False) 
            reg_f.is_staff = False 
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now() 
            reg_f.last_login = datetime.now() 
            reg_f.save()

            return redirect('home')
    else:
        regform = UserCreationForm()

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )
def important(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/important.html',
        {

        }
    )
def blog(request):
     """Renders the blog page."""
     assert isinstance(request, HttpRequest)
     posts = Blog.objects.all() # запрос на выбор всех статей блога из модели

     return render(
          request,
          'app/blog.html',
          {
              'title':'Блог',
              'posts': posts, # передача списка статей в шаблон веб-страницы
              'year':datetime.now().year,

          }
   )
def blogpost(request, parametr):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST": # после отправки данных формы на сервер методом POST
       form = CommentForm(request.POST)
       if form.is_valid():
           comment_f = form.save(commit=False)
           comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
           comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
           comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
           comment_f.save() # сохраняем изменения после добавления полей

           return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария

    else:
       form = CommentForm() # создание формы для ввода комментария

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def newpost(request):
    assert isinstance(request,HttpRequest)
    
    if request.method =="POST":
        blogform = BlogForm(request.POST,request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit= False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
           'blogform':blogform,
           'title': 'Добавить статью блога',

           'year':datetime.now().year,

        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'year':datetime.now().year,
        }
    )

        
