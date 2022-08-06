
from django.urls import path, include

from . import views



app_name = 'reports'

urlpatterns = [
    path('', views.tournaments_list, name='tournaments'),
    path('<int:tournament_id>/register/', views.register, name='register'),
    path('<int:tournament_id>/unregister/', views.unregister, name='unregister'),
    path('<int:tournament_id>/', views.reports_list, name='reports_list'),
    path('<int:tournament_id>/report/', views.report, name='report'),
]