
from django.shortcuts import render

from .models import Tournament



def tournaments_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'reports/tournaments_list.html', {'tournaments': tournaments})