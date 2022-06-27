
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _

from homm.models import Map
from users.models import CustomUser



class Tournament (models.Model):

    min_year_validator = validators.MinValueValidator(2000)
    max_year_validator = validators.MaxValueValidator(2100)

    name_ru = models.CharField(max_length=512)
    shortname_ru = models.CharField(max_length=128)
    name_en = models.CharField(max_length=512)
    shortname_en = models.CharField(max_length=128)
    year = models.IntegerField(validators=[min_year_validator, max_year_validator])
    maps = models.ManyToManyField(Map)
    is_official = models.BooleanField(_('Официальный турнир'), default=True)
    is_private = models.BooleanField(
        _('Закрытый турнир'),
        default=False,
        help_text = _('На этот турнир нет открытой регистрации.')
    )
    forum_thread = models.CharField(
        _('Тема турнира'),
        max_length=51,
        help_text=_('Ссылка на тему турнира на форуме.')
    )
    is_registration_opened = models.BooleanField(_('Регистрация открыта'), default=False)
    is_closed = models.BooleanField(_('Турнир завершен'), default=False)
    players = models.ManyToManyField(CustomUser, through='TournamentPlayer', blank=True)

    def __str__(self):
        return self.shortname_ru



class TournamentPlayer (models.Model):

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime_registered = models.DateTimeField(_('Дата регистрации на турнир'), auto_now_add=True)
    time_available = models.TextField(_('Возможное время игры'), max_length=2048)

    # disqualified = models.BooleanField(_('Игрок снят/снялся'), default=False)
    # banned = models.BooleanField(_('Игрок забанен на следующий сезон'), default=False)
    # ban_duration = models.IntegerField(_('На сколько сезонов забанен игрок'), default=0)
    # comment = models.TextField(_('Комментарий'), max_length=5000, help_text=_('Например, причина снятия/бана.'), blank=True)

    class Meta:
        db_table = 'reports_tournament_players'