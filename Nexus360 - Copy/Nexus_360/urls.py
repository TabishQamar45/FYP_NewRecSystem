from django.urls import path
from .views import HomeView,News_detail_view,Add_article_view,Update_article_view,Delete_article_view,CategoryView
from . import views

#URLconfg
urlpatterns=[

    path('',HomeView.as_view(),name="home"),
    path('article/<int:pk>',News_detail_view.as_view(),name="article_detail"),
    path('add_article/',Add_article_view.as_view(),name="addnews"),
    path('update/article/<int:pk>',Update_article_view.as_view(),name="updateArticle"),
    path('remove/<int:pk>',Delete_article_view.as_view(),name="deleteArticle"),
    path('category/<str:cats>/',CategoryView,name="category"),
    path('search/article',views.searced_view,name="searcedview"),
    path('register',views.signup, name='signup'),

]
