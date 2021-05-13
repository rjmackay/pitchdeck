from io import BytesIO

from django import forms
from django.core.files.base import ContentFile
from pdf2image import convert_from_path

from .models import PitchDeck
from .models import PitchImage


class PitchUploadForm(forms.Form):
    pitch_deck = forms.FileField(required=True)

    def process_pitch(self):
        # send email using the self.cleaned_data dictionary
        upload = self.cleaned_data["pitch_deck"]
        pitch = PitchDeck.objects.create(name=upload.name, original=upload)

        images = convert_from_path(pitch.original.path, fmt="png", size=(800, None))
        for page, image in enumerate(images):
            pitch_image = PitchImage(pitch_deck=pitch, page=page)
            # dest = default_storage.open(f"{upload.name}_{i}.png", "wb+")
            output_file = BytesIO()
            image.save(fp=output_file, format="png")
            pitch_image.image.save(f"{pitch.original.name}.{page}.png", ContentFile(output_file.getvalue()), save=False)
            pitch_image.save()
