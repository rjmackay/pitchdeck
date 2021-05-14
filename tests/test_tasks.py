import os

from django.core.files.base import File
from model_bakery import baker
import pytest

from apps.core.tasks import convert_pitch_to_image


@pytest.mark.django_db
def test_convert_pitch_to_image():
    """Test convert_pitch_to_image task"""
    pwd = os.path.dirname(os.path.abspath(__file__))
    pdf = open(os.path.join(pwd, "wefunder_deck_2021.pdf"), "rb")

    pitch_deck = baker.make("core.PitchDeck")
    pitch_deck.original.save("test.pdf", File(pdf))

    convert_pitch_to_image(pitch_deck.id)

    pitch_deck.refresh_from_db()
    assert pitch_deck.processed
    assert pitch_deck.images.count() == 21

    # Cleanup
    pitch_deck.original.delete()
    for image in pitch_deck.images.all():
        image.image.delete()
