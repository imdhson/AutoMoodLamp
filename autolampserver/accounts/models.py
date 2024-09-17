from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    deviceId = models.CharField(max_length=255, blank=True, null=True)
    sequenceData = models.JSONField(default=dict)

    def add_sequence_data(self, datetime, class_idx, percent):
        if not isinstance(percent, int):
            raise ValueError("Number must be an integer")
        if not isinstance(class_idx, int):
            raise ValueError("Number must be an integer")
        self.sequenceData = models.JSONField(default=dict)
        self.save()

    def get_sequence_data(self):
        return self.sequenceData