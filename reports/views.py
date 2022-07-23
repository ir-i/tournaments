
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Tournament, TournamentPlayer
from .forms import Register



def user_is_registered(tournament, user):

    tournament_player = TournamentPlayer.objects.filter(tournament_id=tournament.id, player=user).first()
    if tournament_player != None:
        return True
    else:
        return False



def tournaments_list(request):

    tournaments = Tournament.objects.all()

    user_can_register = {}
    user_can_unregister = {}
    
    for tournament in tournaments:
        if request.user.is_authenticated:
            user_can_register[tournament.id] = not user_is_registered(tournament, request.user)
        else:
            user_can_register[tournament.id] = False

    for tournament in tournaments:
        if request.user.is_authenticated:
            user_can_unregister[tournament.id] = user_is_registered(tournament, request.user)
        else:
            user_can_unregister[tournament.id] = False

    return render(request, 'reports/tournaments_list.html', {
        'tournaments': tournaments,
        'user_can_register': user_can_register,
        'user_can_unregister': user_can_unregister,
    })



@login_required(login_url='/users/login/')
def register(request, tournament_id):

    tournament = get_object_or_404(Tournament, id=tournament_id)

    if not tournament.allows_to_register:
        return HttpResponse('На этот турнир зарегистрироваться нельзя.')
    elif user_is_registered(tournament, request.user):
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

    if not tournament.allows_to_unregister:
        return HttpResponse('Отменить регистрацию нельзя.')
    elif not user_is_registered(tournament, request.user):
        return HttpResponse('Вы не зарегистрированы на этот турнир.')

    if request.method == 'POST':
        tournament_player = TournamentPlayer.objects.get(tournament_id=tournament_id, player_id=request.user.id)
        tournament_player.delete()
        return redirect('/')

    return render(request, 'reports/unregister.html', {'tournament_id': tournament_id})