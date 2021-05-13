from django import forms
from django.core.files.storage import default_storage
from pdf2image import convert_from_path


class PitchUploadForm(forms.Form):
    pitch_deck = forms.FileField(required=True)

    def process_pitch(self):
        # send email using the self.cleaned_data dictionary
        upload = self.cleaned_data["pitch_deck"]
        dest = default_storage.open(upload.name, 'wb+')
        for chunk in upload.chunks():
            dest.write(chunk)
        dest.close()

        images = convert_from_path(dest.name)
        for i, image in enumerate(images):
            dest = default_storage.open(f"{upload.name}_{i}.png", "wb+")
            image.save(fp=dest.file, format="png")
