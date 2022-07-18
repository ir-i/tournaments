
from django import forms

from .models import TournamentPlayer



class Register (forms.ModelForm):

    class Meta:
        model = TournamentPlayer
        fields = ['time_available']