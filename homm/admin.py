
from django.contrib import admin

from .models import Title, Discipline



class TitleAdmin (admin.ModelAdmin):

    list_display =  ('shortname', 'name')



class DisciplineAdmin (admin.ModelAdmin):

    list_display =  ('shortname', 'name')



admin.site.register(Title, TitleAdmin)
admin.site.register(Discipline, DisciplineAdmin)