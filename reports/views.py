
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Tournament, TournamentPlayer
from .forms import Register


'''
    checks if a user can register to a tournament
    returns:
         0 - can register
        -1 - tournament doesn't allow to register
        -2 - user already registered to the tournament
'''
def user_can_register(tournament, user):

    if tournament.is_closed \
    or tournament.is_private \
    or not tournament.is_registration_opened:
        return -1
    else:
        tournament_player = TournamentPlayer.objects.filter(tournament_id=tournament.id, player=user).first()
        if tournament_player != None:
            return -2
        else:
            return 0



def tournaments_list(request):
    tournaments = Tournament.objects.all()
    return render(request, 'reports/tournaments_list.html', {'tournaments': tournaments})



@login_required(login_url='/users/login/')
def register(request, tournament_id):

    tournament = Tournament.objects.get(id=tournament_id)

    can_register = user_can_register(tournament, request.user)
    if can_register == -1:
        return HttpResponse('На этот турнир зарегистрироваться нельзя.')
    elif can_register == -2:
        return HttpResponse('Вы уже зарегистрированы на этот турнир.')

    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid:
            instance = form.save(commit=False)
            instance.tournament = tournament
            instance.player = request.user
            instance.save()
            return redirect('/')
    else:
        form = Register()

    return render(request, 'reports/register.html', {'form': form, 'tournament_id': tournament_id})