# -*- coding: utf-8 -*-

import os
import re
import cv2
import numpy as np
from ocrdemo import utils


class PreprocessImage:
    def cleanNoises(self, image):
        '''Preprocess image'''
        utils.info('Deskewing the file: {}'.format(image))
        self._rotateFile(image)
        utils.info('Clear shadow of file: {}'.format(image))
        self._cleanShadow(image)

        return True

    def _cleanShadow(self, input_file):
        img = cv2.imread(input_file, -1)
        rgb_planes = cv2.split(img)

        result_planes = []
        result_norm_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(diff_img,
                                     None,
                                     alpha=0,
                                     beta=255,
                                     norm_type=cv2.NORM_MINMAX,
                                     dtype=cv2.CV_8UC1)
            result_planes.append(diff_img)
            result_norm_planes.append(norm_img)

        result = cv2.merge(result_planes)
        cv2.imwrite(input_file, result)

    def _rotateFile(self, input_file):
        image = cv2.imread(input_file)

        # Slice minor border after scan
        w, h, _ = image.shape
        image = image[30:w - 30, 30:h - 30]

        # convert the image to grayscale and flip the foreground
        # and background to ensure foreground is now "white" and
        # the background is "black"
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)

        # threshold the image, setting all foreground pixels to
        # 255 and all background pixels to 0
        thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # grab the (x, y) coordinates of all pixel values that
        # are greater than zero, then use these coordinates to
        # compute a rotated bounding box that contains all
        # coordinates
        coords = np.column_stack(np.where(thresh > 0))
        angle = cv2.minAreaRect(coords)[-1]

        # the `cv2.minAreaRect` function returns values in the
        # range [-90, 0); as the rectangle rotates clockwise the
        # returned angle trends to 0 -- in this special case we
        # need to add 90 degrees to the angle
        if angle < -45:
            angle = -(90 + angle)
        # otherwise, just take the inverse of the angle to make
        # it positive
        else:
            angle = -angle

        # rotate the image to deskew it
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, .8)
        rotated = cv2.warpAffine(image,
                                 M, (w, h),
                                 flags=cv2.INTER_CUBIC,
                                 borderMode=cv2.BORDER_REPLICATE)

        # draw the correction angle on the image so we can validate it
        # cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Slice white space at margin
        gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
        gray = 255 * (gray < 128).astype(np.uint8)
        coords = cv2.findNonZero(gray)
        x, y, w, h = cv2.boundingRect(coords)
        rect = rotated[y:y + h, x:x + w]

        # show the output image
        utils.info("Image {} de-skew with angle: {:.3f}".format(
            input_file, angle))

        # Write image
        cv2.imwrite(input_file, rect)
