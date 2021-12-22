# Nexus360
from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import News_Post,Category
from .forms import addArticleForm,updateArticleForm
from django.template import loader
from django.urls import reverse_lazy
import mysql.connector
from Nexus_360.content_base import get_pred
import numpy as np
import json
# Create your views here.

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="goodboy123",
  database = "nexus360"
)
user_Session=[]
# -- Display all the news on the homePage according to the latest date -- #
class HomeView(ListView):
    model=News_Post
    template_name='home.html'
    ordering=['-date']

    def get_context_data(self,*args,**kwargs):
        category_menu=Category.objects.all()
        context=super(HomeView,self).get_context_data(*args,**kwargs)
        context["category_menu"]=category_menu
        return context

# -- Display the newsDetail with its title and content -- #

class News_detail_view(DetailView):
    model=News_Post
    template_name='news_detail.html'

    def get_context_data(self,*args,**kwargs):
        category_menu=Category.objects.all()
        if self.object.id not in user_Session:
            user_Session.append(self.object.id)
        similar_id,headline=get_pred(user_Session)
        #res = dict(zip(similar_id,headline))
        context=super(News_detail_view,self).get_context_data(*args,**kwargs)
        res = {similar_id[i]: headline[i] for i in range(len(similar_id))}
        context["category_menu"]=category_menu
        # context["id"]=similar_id
        # context["data"]=headline
        context["similar"]=res
        return context

# -- Add a new NewsArticle -- #

class Add_article_view(CreateView):
    model=News_Post
    template_name='add_article.html'
    form_class=addArticleForm

# -- Update an any Article -- #


class Update_article_view(UpdateView):
    model=News_Post
    form_class=updateArticleForm
    template_name='updateArticle.html'

# -- Delete any NewsArticle -- #


class Delete_article_view(DeleteView):
    model=News_Post
    template_name='delete_article.html'
    success_url=reverse_lazy('home')


# -- Search any NewsArticle -- #

def searced_view(request):
    if request.method=='POST':
        searched=request.POST.get('searched')
        newsSearch=News_Post.objects.filter(title__icontains=searched)
        return render(request,'search_article.html',{'searched':searched ,'newsSearch':newsSearch})
    else:
        return render(request,'search_article.html',{})

#-------Category-View--------#
def CategoryView(request,cats):
    news_category=Category.objects.all()
    category_post=News_Post.objects.filter(category=cats)
    return render(request,'categories.html',{'cats':cats.title(),'category_post':category_post,news_category:'news_category'})




def signup(request):
    return render(request,'SignUp.html')







# import mysql.connector
#
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="goodboy123",
#   database = "nexus360"
# )
#
# cursor = mydb.cursor()
# cursor.execute("select * from actor")
# result = cursor.fetchall()
# for x in result:
#     print (x)
