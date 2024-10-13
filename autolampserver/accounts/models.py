from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    sequenceData = models.JSONField(default=dict)
    conversationData = models.JSONField(default=dict)

    def add_sequence_data(self, timestamp, class_idx, class_name, percent, volume):
        if not isinstance(class_idx, int) or not isinstance(percent, int) or not isinstance(volume, (float)):
            raise ValueError("class_idx and percent must be integers, and volume must be a float")
        if not isinstance(class_name, str):
            raise ValueError("class_name must be a string")
        
        self.sequenceData[timestamp] = {
            "class_idx": class_idx,
            "class_name": class_name,
            "percent": percent,
            "volume": volume
        }
        self.save()

    def get_sequence_data(self):
        return self.sequenceData

    def add_conversation_data(self, timestamp, text, emotion_score):
        if not isinstance(timestamp, str) or not isinstance(text, str) or not isinstance(emotion_score, str):
            raise ValidationError("Invalid data types for conversation data")
        
        self.conversationData[timestamp] = {
            "text": text,
            "emotion_score": emotion_score
        }
        self.save()

    def get_conversation_data(self):
        return self.conversationData