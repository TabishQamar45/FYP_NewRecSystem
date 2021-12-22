from django.contrib import admin

# Register your models here.
from .models import News_Post,Category

admin.site.register(News_Post)
admin.site.register(Category)
