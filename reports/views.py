
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Tournament
from .forms import Register



def tournaments_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'reports/tournaments_list.html', {'tournaments': tournaments})


@login_required(login_url='/users/login/')
def register(request, tournament_id):

    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid:
            instance = form.save(commit=False)
            tournament = Tournament.objects.get(id=tournament_id)
            instance.tournament = tournament
            instance.player = request.user
            instance.save()
            return redirect('/')
            # return HttpResponse(instance.tournament)
    else:
        form = Register()

    return render(request, 'reports/register.html', {'form': form, 'tournament_id': tournament_id})