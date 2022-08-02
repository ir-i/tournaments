
from django import forms

from .models import TournamentPlayer, Report, Game



class Register (forms.ModelForm):

    class Meta:
        model = TournamentPlayer
        fields = ['time_available']



class ReportForm (forms.ModelForm):

    def __init__(self, tournament, player1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['player2'].queryset = tournament.tournamentplayer_set.exclude(player=player1)


    class Meta:
        model = Report
        fields = ['player2', 'player1_comment']



class GameForm (forms.ModelForm):

    class Meta:
        model = Game
        fields = ['faction1', 'hero1', 'faction2', 'hero2', 'winner']