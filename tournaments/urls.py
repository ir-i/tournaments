
from django.urls import path, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from reports import views as reports_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('reports/', include('reports.urls')),
    path('', reports_views.tournaments_list, name='home')
]


urlpatterns += staticfiles_urlpatterns()