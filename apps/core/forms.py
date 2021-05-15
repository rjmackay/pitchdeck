from django import forms
from django.core.validators import FileExtensionValidator

from .models import PitchDeck
from .tasks import convert_pitch_to_image


class PitchUploadForm(forms.Form):
    pitch_deck = forms.FileField(required=True, validators=[FileExtensionValidator(allowed_extensions=["pdf", "pptx"])])

    def process_pitch(self):
        # Save uploaded image
        upload = self.cleaned_data["pitch_deck"]
        pitch = PitchDeck.objects.create(name=upload.name, original=upload)
        # Queue conversion to images
        convert_pitch_to_image.delay(pitch.id)
