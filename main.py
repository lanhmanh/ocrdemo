# -*- coding: utf-8 -*-

import json
import os
import sys
import time
import click
import pathlib

from ocrdemo import utils
from ocrdemo.preprocessing import PreprocessImage
from ocrdemo.constants import GlobalConstants
from tesserocr import PyTessBaseAPI, PSM, OEM


@click.command()
@click.option('-i',
              '--input',
              help='Input PNG, JPEG, PDF file types only.',
              required=True)
@click.option('-o', '--output', help='Path output file.', required=False)
@click.option('-v', '--verbose', count=True, help='Debug for more detail.')


def handler(input, output, verbose):
    utils.setLevel(verbose)

    validate(input, output)
    f = open(output, 'a')
    list_images = utils.getImages(input)
    preprocess = PreprocessImage()
    with PyTessBaseAPI(oem=OEM.TESSERACT_CUBE_COMBINED) as api:
        for image in list_images:
            # Pre-process the image
            preprocess.cleanNoises(image)

            # Process OCR
            api.Clear()
            api.SetImageFile(image)

            utils.info('Process OCR for image: {}'.format(image))
            text = api.GetUTF8Text()
            utils.info("Text Output: %s" % text)
            f.write(text)

    f.close()


def validate(input_file, output_file):
    '''
    Check if validate file types
    '''
    allowed_file_ext = {".pdf", ".jpg", ".jpeg", ".png"}
    if (input_file == ''):
        utils.error('Input file is required')
        raise RuntimeError('Input file is required')

    file_path = pathlib.Path(input_file)
    if file_path.exists() is False or file_path.is_file() is False:
        utils.error("Input file is not exists")
        raise RuntimeError('Input file is not exists')

    if file_path.suffix.lower() not in allowed_file_ext:
        utils.error("Input file is not allowed")
        raise RuntimeError('Input file is not allowed')

    return True


if __name__ == "__main__":
    try:
        start = time.time()
        utils.info("App Starting....")
        handler()
    except Exception as e:
        utils.error(
            "%s.%s [%s] cause Exception %s :" %
            (__name__, sys._getframe().f_code.co_name,
             sys._getframe().f_lineno, sys.exc_info()[0]), e)
    finally:
        elapsed_time = time.time() - start
    utils.info("elapsed_time:%s" % (elapsed_time) + "[sec]. Process Done!")
