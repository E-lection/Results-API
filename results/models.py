# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Vote(models.Model):
    constituency = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    candidate_first_name = models.CharField(max_length=100)
    candidate_last_name = models.CharField(max_length=200)

    def __str__(self):
        return self.constituency + ' - ' + self.party + ' - ' + self.candidate_last_name
