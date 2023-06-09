
from django.contrib import admin

from . import models



class TitleAdmin (admin.ModelAdmin):

    list_display =  ('shortname', 'name')



class DisciplineAdmin (admin.ModelAdmin):

    list_display =  ('shortname', 'name')



class MapAdmin (admin.ModelAdmin):

    list_display =  ('shortname', 'name')



class FactionAdmin (admin.ModelAdmin):

    list_display =  ('name_ru', 'name_en')



class HeroAdmin (admin.ModelAdmin):

    list_display =  ('name_ru', 'name_en')



admin.site.register(models.Title, TitleAdmin)
admin.site.register(models.Discipline, DisciplineAdmin)
admin.site.register(models.Map, MapAdmin)
admin.site.register(models.Faction, FactionAdmin)
admin.site.register(models.Hero, HeroAdmin)