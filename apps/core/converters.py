import logging
import os
import subprocess
import tempfile
from typing import List

from PIL.Image import Image
from pdf2image import convert_from_bytes
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)


class Converters:
    registry = {}

    @classmethod
    def register(cls, extension):
        def inner_wrapper(wrapped_class: ConverterBase):
            if extension in cls.registry:
                logger.warning("Converter %s already exists. Will replace it", extension)
            cls.registry[extension] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def convert(cls, fp):
        filename_ext = os.path.splitext(os.path.basename(fp.name))[1].lstrip(".")
        if filename_ext not in cls.registry:
            logger.warning("Could not find converter for %s", filename_ext)
            return []

        converter = cls.registry[filename_ext]()
        return converter.convert(fp)


class ConverterBase(object):
    def convert(self, fp) -> List[Image]:
        return []


@Converters.register("pdf")
class PDFConverter(ConverterBase):
    def convert(self, fp):
        return convert_from_bytes(fp.read(), fmt="png", size=(800, None))


@Converters.register("pptx")
class PPTConverter(ConverterBase):
    def convert(self, fp):
        with tempfile.TemporaryDirectory() as tmp_dirname:
            temp_input_path = os.path.join(tmp_dirname, fp.name)
            temp_input = open(temp_input_path, "wb")
            for chunk in fp.chunks():
                temp_input.write(chunk)
            temp_input.close()

            command_list = ["soffice", "--headless", "--convert-to", "pdf", temp_input_path]
            try:
                subprocess.run(command_list, cwd=tmp_dirname, check=True, timeout=120)
            except subprocess.CalledProcessError as e:
                logger.warning("PPTX conversion failed: %s", e.stderr)
                return []

            filename_bare = os.path.splitext(temp_input_path)[0]
            logger.info(f"{filename_bare}.pdf")
            return convert_from_path(f"{filename_bare}.pdf", fmt="png", size=(800, None))
