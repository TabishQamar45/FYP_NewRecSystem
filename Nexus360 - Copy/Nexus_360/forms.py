from django import forms
from .models import News_Post,Category

choices=Category.objects.all().values_list('name','name')


choices_list=[]

for choice in choices:
    choices_list.append(choice)

class addArticleForm(forms.ModelForm):
    class Meta:
        model=News_Post

        fields=('title','News_content','date','author','category')

        widgets={
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':choices}),
            'News_content': forms.Textarea(attrs={'class':'form-control'}),
            'author': forms.Select(attrs={'class':'form-control'}),
            'category': forms.Select(choices=choices_list,attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class':'form-control'}),

        }

class updateArticleForm(forms.ModelForm):
    class Meta:
        model=News_Post

        fields=('title','News_content')

        widgets={
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'News_content': forms.Textarea(attrs={'class':'form-control'}),

        }
