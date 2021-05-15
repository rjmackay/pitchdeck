from io import BytesIO
import logging

from django.core.files.base import ContentFile
from django_rq import job

from .converters import Converters
from .models import PitchDeck
from .models import PitchImage

logger = logging.getLogger(__name__)


@job
def convert_pitch_to_image(pitch_id):
    logger.info("Start converting pitch: %s", pitch_id)
    pitch = PitchDeck.objects.get(pk=pitch_id)
    images = Converters.convert(pitch.original)
    logger.info("Pitch converted, saving %s images", len(images))
    for page, image in enumerate(images):
        pitch_image = PitchImage(pitch_deck=pitch, page=page)
        # dest = default_storage.open(f"{upload.name}_{i}.png", "wb+")
        output_file = BytesIO()
        image.save(fp=output_file, format="png")
        pitch_image.image.save(f"{pitch.original.name}.{page}.png", ContentFile(output_file.getvalue()), save=False)
        pitch_image.save()

    pitch.processed = True
    pitch.save()
    logger.info("Finished converting pitch: %s", pitch_id)
