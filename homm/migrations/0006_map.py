# Generated by Django 4.0.5 on 2022-06-23 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homm', '0005_alter_hero_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('shortname', models.CharField(max_length=128)),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='homm.discipline')),
            ],
        ),
    ]
