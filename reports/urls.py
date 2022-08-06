
from django.urls import path, include

from . import views



app_name = 'reports'

urlpatterns = [
    path('', views.tournaments_list, name='tournaments'),
    path('<int:tournament_id>/', views.reports_list, name='reports_list'),
    path('<int:tournament_id>/players', views.players_list, name='players-list'),
    path('<int:tournament_id>/register/', views.register, name='register'),
    path('<int:tournament_id>/unregister/', views.unregister, name='unregister'),
    path('<int:tournament_id>/report/', views.report, name='report'),
    path('reports/<int:report_id>/confirm', views.confirm_report, name='confirm-report'),
    path('reports/<int:report_id>/decline', views.decline_report, name='decline-report'),
]