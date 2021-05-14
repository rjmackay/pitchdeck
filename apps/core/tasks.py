from io import BytesIO

from django.core.files.base import ContentFile
from django_rq import job
from pdf2image import convert_from_bytes

from .models import PitchDeck
from .models import PitchImage


@job
def convert_pitch_to_image(pitch_id):
    pitch = PitchDeck.objects.get(pk=pitch_id)
    images = convert_from_bytes(pitch.original.read(), fmt="png", size=(800, None))
    for page, image in enumerate(images):
        pitch_image = PitchImage(pitch_deck=pitch, page=page)
        # dest = default_storage.open(f"{upload.name}_{i}.png", "wb+")
        output_file = BytesIO()
        image.save(fp=output_file, format="png")
        pitch_image.image.save(f"{pitch.original.name}.{page}.png", ContentFile(output_file.getvalue()), save=False)
        pitch_image.save()

    pitch.processed = True
    pitch.save()
