from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from datetime import date
from ckeditor.fields import RichTextField

#---------Creating the tables-------#
#---------Category Table---------#

class Category(models.Model):
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('home')

# -----UserAccount Table-----#

class UserAccount (models.Model):
    user_id=models.CharField(max_length=100, null=False , primary_key=True)
    email=models.EmailField(null=True)
    contact_no=models.CharField(max_length=13)
    password=models.CharField(max_length=100)


# -----Table column of NewsArticles

class News_Post(models.Model):
    title=models.CharField(max_length=1000)
    # News_content=models.TextField()
    News_content=RichTextField(blank=True,null=True)
    date=models.DateField(default='DEFAULT VALUE')
    #post_date=models.DateField(auto_now_add=True)

    author=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.CharField(max_length=30,default='Politics')
    link=models.CharField(max_length=250,default='link_not_available')
    source=models.CharField(max_length=250,default='Source not available')
    dateOfExtraction=models.DateField()
    
    def __str__(self):
        return self.title + ' | '+ str(self.author)
    def get_absolute_url(self):
        return reverse('home')
