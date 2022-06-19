
from django.contrib import admin

from .models import Title



class TitleAdmin (admin.ModelAdmin):

    list_display =  ('shortname', 'name')


admin.site.register(Title, TitleAdmin)