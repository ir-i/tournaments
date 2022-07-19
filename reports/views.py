
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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



'''
    checks if a user can sign out from a tournament
    returns:
         0 - can sign out
        -1 - tournament doesn't allow to sign out
        -2 - user is not registered to the tournament
'''
def user_can_unregister(tournament, user):

    if tournament.has_started \
    or tournament.is_closed \
    or tournament.is_private \
    or not tournament.is_registration_opened:
        return -1
    else:
        tournament_player = TournamentPlayer.objects.filter(tournament_id=tournament.id, player=user).first()
        if tournament_player == None:
            return -2
        else:
            return 0



def tournaments_list(request):

    tournaments = Tournament.objects.all()

    can_register = {}
    can_unregister = {}

    if request.user.is_authenticated:
        for tournament in tournaments:
            can_register[tournament.id] = user_can_register(tournament, request.user)

        can_unregister = {}
        for tournament in tournaments:
            can_unregister[tournament.id] = user_can_unregister(tournament, request.user)        

    return render(request, 'reports/tournaments_list.html', {
        'tournaments': tournaments,
        'can_register': can_register,
        'can_unregister': can_unregister,
    })



@login_required(login_url='/users/login/')
def register(request, tournament_id):

    tournament = get_object_or_404(Tournament, id=tournament_id)

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



@login_required(login_url='/users/login/')
def unregister(request, tournament_id):

    tournament = get_object_or_404(Tournament, id=tournament_id)

    can_unregister = user_can_unregister(tournament, request.user)
    if can_unregister == -1:
        return HttpResponse('Отменить регистрацию нельзя.')
    elif can_unregister == -2:
        return HttpResponse('Вы не зарегистрированы на этот турнир.')

    if request.method == 'POST':
        tournament_player = TournamentPlayer.objects.get(tournament_id=tournament_id, player_id=request.user.id)
        tournament_player.delete()
        return redirect('/')

    return render(request, 'reports/unregister.html', {'tournament_id': tournament_id})