
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from .models import Tournament, TournamentPlayer, Report, Game
from .forms import Register, ReportForm, GameForm, GameWithMapForm



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

    return render(request, 'reports/register.html', {'form': form, 'tournament': tournament})



@login_required(login_url='/users/login/')
def unregister(request, tournament_id):

    tournament = get_object_or_404(Tournament, id=tournament_id)

    if not tournament.allows_to_unregister:
        return HttpResponse('Отменить регистрацию нельзя.')
    elif not user_is_registered(tournament, request.user):
        return HttpResponse('Вы не зарегистрированы на этот турнир.')

    if request.method == 'POST':
        tournament_player = TournamentPlayer.objects.get(tournament=tournament, player=request.user)
        tournament_player.delete()
        return redirect('/')

    return render(request, 'reports/unregister.html', {'tournament': tournament})



def reports_list(request, tournament_id):

    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.user.is_authenticated:
        user_can_report = user_is_registered(tournament, request.user)
    else:
        user_can_report = False

    reports_list = Report.objects.filter(tournament=tournament).order_by('-datetime_created')

    return render(request, 'reports/tournament.html', {
        'tournament': tournament,
        'user_can_report': user_can_report,
        'reports_list': reports_list
    })



@login_required(login_url='/users/login/')
def report(request, tournament_id):

    tournament = get_object_or_404(Tournament, id=tournament_id)

    if (tournament.maps.count() > 1):
        has_multiple_maps = True
    else:
        has_multiple_maps = False

    if (has_multiple_maps):
        GameFormSet = modelformset_factory(Game, form=GameWithMapForm, extra=7)
    else:
        GameFormSet = modelformset_factory(Game, form=GameForm, extra=7)

    if not tournament.allows_to_report:
        return HttpResponse('Нельзя оставить отчет об игре на этом турнире.')
    elif not user_is_registered(tournament, request.user):
        return HttpResponse('Вы не зарегистрированы на этот турнир.')

    if request.method == 'POST':
        # проверить, что полученный оппонент зарегистрирован на турнир
        report_form = ReportForm(tournament, request.user, request.POST)
        game_formset = GameFormSet(request.POST)
        if (report_form.is_valid() and game_formset.is_valid()):
            report = report_form.save(commit=False)
            report.author = request.user
            report.tournament = tournament
            report.player1 = tournament.tournamentplayer_set.get(player=request.user)
            report.is_commited = True   # в прекрасном будущем пользователь сможет составлять черновик отчета, и пока он его не подтвердит, is_commited будет False (значение по умолчанию); а пока что принудительно ставится True
            report.save()
            games = game_formset.save(commit=False)
            for game in games:
                game.report = report
                if(not has_multiple_maps):
                    game.map = tournament.maps.all()[0]
                game.save()
            return redirect('/reports/' + str(tournament.id) + '/reports-list')
    
    else:
        report_form = ReportForm(tournament, request.user)
        if (has_multiple_maps):
            game_formset = GameFormSet(queryset=Game.objects.none(), form_kwargs={'tournament': tournament})
        else:
            game_formset = GameFormSet(queryset=Game.objects.none())

    return render(request, 'reports/report.html', {
        'tournament': tournament,
        'report_form': report_form,
        'game_formset': game_formset,
    })