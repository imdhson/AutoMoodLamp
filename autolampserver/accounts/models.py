from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    deviceId = models.CharField(max_length=255, blank=True, null=True)
    sequenceData = models.JSONField(default=dict)

    def add_sequence_data(self, timestamp, class_idx, class_name, percent):
        if not isinstance(percent, int) or not isinstance(class_idx, int) or not isinstance(class_name, str):
            raise ValueError("class_idx and percent must be integers")
        self.sequenceData[timestamp] = {"class_idx": class_idx, "percent": percent, "class_name": class_name}
        self.save()

    def get_sequence_data(self):
        return self.sequenceData