from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from model_bakery import baker
import pytest

from apps.core.models import PitchDeck


@pytest.mark.django_db
def test_pitch_detail(client):
    """Check that pitch detail renders the latest pitch"""
    resp = client.get(reverse("home"))
    assert resp.status_code == 302

    pitch_deck = baker.make("core.PitchDeck", _create_files=True, processed=True)
    baker.make("core.PitchImage", pitch_deck=pitch_deck, _create_files=True)
    baker.make("core.PitchImage", pitch_deck=pitch_deck, _create_files=True)

    resp = client.get(reverse("home"))
    assert resp.status_code == 200
    assert bytes(pitch_deck.original.url, "utf-8") in resp.content
    assert bytes(pitch_deck.images.all()[0].image.url, "utf-8") in resp.content

    # Cleanup
    pitch_deck.original.delete()
    for image in pitch_deck.images.all():
        image.image.delete()


@pytest.mark.django_db
def test_pitch_detail_not_processed(client):
    """Check that pitch detail renders the latest pitch"""
    baker.make("core.PitchDeck", processed=False)

    resp = client.get(reverse("home"))
    assert resp.status_code == 200
    assert b"still being processed" in resp.content


@pytest.mark.django_db
@mock.patch("apps.core.forms.convert_pitch_to_image")
def test_pitch_upload(mock_convert, client):
    """Check that pitch upload form works"""
    resp = client.get(reverse("upload"))
    assert resp.status_code == 200

    resp = client.post(reverse("upload"), {})
    assert resp.status_code == 200
    assert len(resp.context["form"].errors) == 1
    assert not mock_convert.called

    f = SimpleUploadedFile("file.pdf", b"junk_content")
    resp = client.post(reverse("upload"), {"pitch_deck": f})

    pitch = PitchDeck.objects.all().first()

    assert resp.status_code == 302
    mock_convert.delay.assert_called_with(pitch.id)

    # Cleanup
    pitch.original.delete()
    for image in pitch.images.all():
        image.image.delete()
