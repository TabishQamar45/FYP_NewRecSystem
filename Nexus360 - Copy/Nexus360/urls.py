
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Nexus_360/',include('Nexus_360.urls')),
    path('members/',include('members.urls')),
    path('members/',include('django.contrib.auth.urls')),

]
