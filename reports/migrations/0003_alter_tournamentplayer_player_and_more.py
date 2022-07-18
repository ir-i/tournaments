# Generated by Django 4.0.5 on 2022-07-14 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0002_match_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentplayer',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tournamentplayer',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reports.tournament'),
        ),
        migrations.AddConstraint(
            model_name='tournamentplayer',
            constraint=models.UniqueConstraint(fields=('tournament', 'player'), name='unique_tournament_player'),
        ),
    ]