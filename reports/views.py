
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from .models import Tournament, TournamentPlayer, Report, Game
from .forms import ConfirmReportForm, Register, ReportForm, GameForm, GameWithMapForm



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



def tournament(request, tournament_id):

    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.user.is_authenticated:
        user_can_report = user_is_registered(tournament, request.user)
        user_can_register = not user_is_registered(tournament, request.user)
        user_can_unregister = user_is_registered(tournament, request.user)
    else:
        user_can_report = False
        user_can_register = False
        user_can_unregister = False

    reports_list = Report.objects.filter(tournament=tournament).order_by('-datetime_created')
    players_list = tournament.players.all()

    return render(request, 'reports/tournament.html', {
        'tournament': tournament,
        'user_can_report': user_can_report,
        'user_can_register': user_can_register,
        'user_can_unregister': user_can_unregister,
        'reports_list': reports_list,
        'players_list': players_list
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
            return redirect('/reports/' + str(tournament.id))
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
        return redirect('/reports/' + str(tournament.id))

    return render(request, 'reports/unregister.html', {'tournament': tournament})



@login_required(login_url='/users/login/')
def add_report(request, tournament_id):

    tournament = get_object_or_404(Tournament, id=tournament_id)

    if (tournament.maps.count() > 1):
        has_multiple_maps = True
    else:
        has_multiple_maps = False

    if request.method == 'POST':
        extra = request.POST['form-TOTAL_FORMS']
    else:
        extra = 1

    if (has_multiple_maps):
        GameFormSet = modelformset_factory(Game, form=GameWithMapForm, extra=extra)
    else:
        GameFormSet = modelformset_factory(Game, form=GameForm, extra=extra)

    if not tournament.allows_to_report:
        return HttpResponse('Нельзя оставить отчет об игре на этом турнире.')
    elif not user_is_registered(tournament, request.user):
        return HttpResponse('Вы не зарегистрированы на этот турнир.')

    if request.method == 'POST':
        # проверить, что полученный оппонент зарегистрирован на турнире
        report_form = ReportForm(tournament, request.user, request.POST)
        game_formset = GameFormSet(request.POST)
        print(game_formset.extra)
        if (report_form.is_valid() and game_formset.is_valid()):
            report = report_form.save(commit=False)
            report.author = request.user
            report.tournament = tournament
            report.player1 = tournament.tournamentplayer_set.get(player=request.user)
            report.is_commited = True   # в прекрасном будущем пользователь сможет составлять черновик отчета, и пока он его не подтвердит, is_commited будет False (значение по умолчанию); а пока что принудительно ставится True
            report.save()
            print(game_formset.errors)
            games = game_formset.save(commit=False)
            print(game_formset.errors)
            print(games)
            for game in games:
                print('---!!!---')
                print(game)
                game.report = report
                if(not has_multiple_maps):
                    game.map = tournament.maps.all()[0]
                game.save()
            return redirect('/reports/' + str(tournament.id))
    
    else:
        report_form = ReportForm(tournament, request.user)
        if (has_multiple_maps):
            game_formset = GameFormSet(queryset=Game.objects.none(), form_kwargs={'tournament': tournament})
        else:
            game_formset = GameFormSet(queryset=Game.objects.none())

    return render(request, 'reports/add-report.html', {
        'tournament': tournament,
        'report_form': report_form,
        'game_formset': game_formset,
    })



@login_required(login_url='/users/login/')
def confirm_report(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    if not report.player2.player == request.user or not report.is_confirmed == None:
        return HttpResponse('Вы не можете подтвердить или отклонить этот отчет.')

    if request.method == 'POST':
        form = ConfirmReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.is_confirmed = True
            report.save()
            return redirect('/reports/' + str(report.tournament.id))


    form = ConfirmReportForm(instance=report)

    return render(request, 'reports/confirm-report.html', {'report': report, 'form': form})



@login_required(login_url='/users/login/')
def decline_report(request, report_id):

    report = get_object_or_404(Report, id=report_id)

    if not report.player2.player == request.user or not report.is_confirmed == None:
        return HttpResponse('Вы не можете подтвердить или отклонить этот отчет.')

    if request.method == 'POST':
        form = ConfirmReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.is_confirmed = False
            report.save()
            return redirect('/reports/' + str(report.tournament.id))

    form = ConfirmReportForm(instance=report)

    return render(request, 'reports/confirm-report.html', {'report': report, 'form': form})