
from django.urls import path, include

from . import views



app_name = 'reports'

urlpatterns = [
    path('', views.tournaments_list, name='tournaments'),
    path('<int:tournament_id>/', views.tournament, name='tournament'),
    path('<int:tournament_id>/register/', views.register, name='register'),
    path('<int:tournament_id>/unregister/', views.unregister, name='unregister'),
    path('<int:tournament_id>/add-report/', views.add_report, name='add-report'),
    path('reports/<int:report_id>/confirm', views.confirm_report, name='confirm-report'),
    path('reports/<int:report_id>/decline', views.decline_report, name='decline-report'),
]