
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _

from homm.models import Map, Faction, Hero
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
    registration_is_opened = models.BooleanField(_('Регистрация открыта'), default=False)
    has_started = models.BooleanField(_('Турнир стартовал'), default=False)
    is_closed = models.BooleanField(_('Турнир завершен'), default=False)
    players = models.ManyToManyField(CustomUser, through='TournamentPlayer', blank=True)

    def __str__(self):
        return self.shortname_ru


    @property
    def allows_to_register(self):
        if (not self.is_closed and not self.is_private and self.registration_is_opened):
            return True
        else:
            return False


    @property
    def allows_to_unregister(self):
        if (not self.is_closed and not self.is_private and not self.has_started and self.registration_is_opened):
            return True
        else:
            return False


    @property
    def allows_to_report(self):
        if (not self.is_closed and self.has_started):
            return True
        else:
            return False



class TournamentPlayer (models.Model):

    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)
    player = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    datetime_registered = models.DateTimeField(_('Дата регистрации на турнир'), auto_now_add=True)
    time_available = models.TextField(_('Возможное время игры'), max_length=2048)

    # disqualified = models.BooleanField(_('Игрок снят/снялся'), default=False)
    # banned = models.BooleanField(_('Игрок забанен на следующий сезон'), default=False)
    # ban_duration = models.IntegerField(_('На сколько сезонов забанен игрок'), default=0)
    # comment = models.TextField(_('Комментарий'), max_length=5000, help_text=_('Например, причина снятия/бана.'), blank=True)


    def __str__(self):
        return self.player.username


    class Meta:
        db_table = 'reports_tournament_players'
        constraints = [
            models.UniqueConstraint(fields=['tournament', 'player'], name='unique_tournament_player')
        ]



class Report (models.Model):

    min_techresult_validator = validators.MinValueValidator(0)
    max_techresult_validator = validators.MaxValueValidator(2)

    datetime_created = models.DateTimeField(_('Дата начала отчета'), auto_now_add=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    player1 = models.ForeignKey(TournamentPlayer, on_delete=models.PROTECT, related_name='player1_set')
    player2 = models.ForeignKey(TournamentPlayer, on_delete=models.PROTECT, related_name='player2_set')
    techresult = models.SmallIntegerField(default=0, validators=[min_techresult_validator, max_techresult_validator])
    is_commited = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(null=True)       # NULL - еще не подтвержден, False - отклонен, True - подтвержден
    datetime_commited = models.DateTimeField(_('Дата завершения отчета'), null=True)
    datetime_confirmed = models.DateTimeField(_('Дата подтверждения/отклонения отчета'), null=True)
    player1_comment = models.TextField(max_length=5000, blank=True)
    player2_comment = models.TextField(max_length=5000, blank=True)



class Game (models.Model):

    min_winner_validator = validators.MinValueValidator(1)
    max_winner_validator = validators.MaxValueValidator(2)

    datetime = models.DateTimeField(_('Дата добавления игры'), auto_now_add=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.PROTECT)
    faction1 = models.ForeignKey(Faction, null=True, blank=True, on_delete=models.PROTECT, related_name='faction1_set')
    faction2 = models.ForeignKey(Faction, null=True, blank=True, on_delete=models.PROTECT, related_name='faction2_set')
    hero1 = models.ForeignKey(Hero, null=True, blank=True, on_delete=models.PROTECT, related_name='hero1_set')
    hero2 = models.ForeignKey(Hero, null=True, blank=True, on_delete=models.PROTECT, related_name='hero2_set')
    winner = models.SmallIntegerField(validators=[min_winner_validator, max_winner_validator])