import os

import PIL
from pdf2image import convert_from_path


def test_pdf2image():
    """Simple test to confirm pdf2image is functioning as expected"""
    pwd = os.path.dirname(os.path.abspath(__file__))
    images = convert_from_path(os.path.join(pwd, "wefunder_deck_2021.pdf"))
    assert len(images) == 21
    assert isinstance(images[0], PIL.PpmImagePlugin.PpmImageFile)
