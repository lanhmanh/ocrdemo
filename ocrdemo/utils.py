# -*- coding: utf-8 -*-

import sys
import pathlib
import tempfile
from datetime import datetime
from logging import DEBUG, ERROR, INFO, StreamHandler, getLogger
from os import path
from typing import Set
from pdf2image import convert_from_path

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)


def setLevel(verbose=0):
    if (verbose != 0):
        logger.setLevel(DEBUG)
        handler.setLevel(DEBUG)
        logger.addHandler(handler)


def info(*arg):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info("{0} {1} {2}".format(date,
                                     sys._getframe().f_code.co_name, arg))


def error(*arg):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.error("{0} {1} {2}".format(date,
                                      sys._getframe().f_code.co_name, arg))
    logger.exception('Error : %s', arg)


def debug(*arg):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.debug("{0} {1} {2}".format(date,
                                      sys._getframe().f_code.co_name, arg))


def getImages(input_file) -> Set[str]:
    list_images = set({})
    file_path = pathlib.Path(input_file)

    if file_path.suffix.lower() == '.pdf':
        logger.info('Convert pdf to images')
        images = convert_from_path(input_file)
        for idx, image in enumerate(images):
            image_name = '{}-{}.jpg'.format(file_path.stem, str(idx))
            logger.info('Convert PDF page: %d into image: %s' %
                        (idx, image_name))
            temp_file = path.join(tempfile.gettempdir(), image_name)

            list_images.add(temp_file)
            image.save(temp_file, 'JPEG')
    else:
        list_images.add(input_file)

    return list_images
