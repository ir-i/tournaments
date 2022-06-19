
from django.db import models



class Title (models.Model):

    name = models.CharField(max_length=512)
    shortname = models.CharField(max_length=128)

    def __str__(self):
        return self.name