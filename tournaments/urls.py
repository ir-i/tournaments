
from django.urls import path, include
from django.contrib import admin

from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('reports/', include('reports.urls')),
    path('', views.base_layout, name='base_layout')
]
