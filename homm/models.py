
from django.db import models



class Title (models.Model):

    name = models.CharField(max_length=512)
    shortname = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Discipline (models.Model):

    name = models.CharField(max_length=512)
    shortname = models.CharField(max_length=128)
    title = models.ForeignKey(Title, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Faction (models.Model):

    name_ru = models.CharField(max_length=128)
    name_en = models.CharField(max_length=128)
    title = models.ForeignKey(Title, on_delete=models.PROTECT)

    def __str__(self):
        return self.name_ru


class Hero (models.Model):

    name_ru = models.CharField(max_length=128)
    name_en = models.CharField(max_length=128)
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT)
    disciplines = models.ManyToManyField(Discipline)

    class Meta:
        verbose_name_plural = 'heroes'

    def __str__(self):
        return self.name_ru