from django.db import models
from authentication.models import HitmanProfile
from django.utils import timezone


class HitAssignation(models.Model):
    assignee = models.ForeignKey(
               HitmanProfile,
               null=True,
               on_delete=models.DO_NOTHING,
               related_name='Assignee')
    creator = models.ForeignKey(
              HitmanProfile,
              on_delete=models.DO_NOTHING,
              related_name='Creator')
    target_name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    is_completed = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.assignee} - {self.creator} - {self.target_name} - {self.description} - {self.is_completed} - {self.date}"