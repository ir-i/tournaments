
from django.contrib import admin

from . import models



class TournamentAdmin (admin.ModelAdmin):

    list_display =  ('shortname_ru', 'name_ru')



admin.site.register(models.Tournament, TournamentAdmin)
