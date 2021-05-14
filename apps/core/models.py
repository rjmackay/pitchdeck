from django.db import models
from model_utils.models import TimeStampedModel


class PitchDeck(TimeStampedModel):
    name = models.CharField(max_length=255)
    original = models.FileField()
    processed = models.BooleanField(default=False)


class PitchImage(models.Model):
    class Meta:
        ordering = ["page"]

    pitch_deck = models.ForeignKey(PitchDeck, on_delete=models.CASCADE, related_name="images")
    page = models.IntegerField()
    image = models.ImageField()
