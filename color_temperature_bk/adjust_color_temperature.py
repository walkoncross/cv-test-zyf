#! /usr/bin/env python
# Ref: https://stackoverflow.com/questions/11884544/setting-color-temperature-for-a-given-image-like-in-photoshop

# You've already found a table of RGB equivalents for each color temperature, but you didn't say where so I found my own: http://www.vendian.org/mncharity/dir3/blackbody/

# A natural scene reflects light proportionately to the color of the light that strikes it. This means a simple linear translation should produce the desired effect. If we assume that the existing image is already white balanced so that pure white is (255,255,255) then it's just a matter of multiplying each of the r,g,b values at each pixel by the proportions corresponding to a color temperature.

# Here's sample code in Python. The multiplication is done indirectly with a matrix.

import sys
import os
import os.path as osp

from PIL import Image
import numpy as np
import cv2


kelvin_table = {
    1000: (255,56,0),
    1500: (255,109,0),
    2000: (255,137,18),
    2500: (255,161,72),
    3000: (255,180,107),
    3500: (255,196,137),
    4000: (255,209,163),
    4500: (255,219,186),
    5000: (255,228,206),
    5500: (255,236,224),
    6000: (255,243,239),
    6500: (255,249,253),
    7000: (245,243,255),
    7500: (235,238,255),
    8000: (227,233,255),
    8500: (220,229,255),
    9000: (214,225,255),
    9500: (208,222,255),
    10000: (204,219,255)}


def convert_temp(image, temp):
    r, g, b = kelvin_table[temp]
    matrix = ( r / 255.0, 0.0, 0.0, 0.0,
               0.0, g / 255.0, 0.0, 0.0,
               0.0, 0.0, b / 255.0, 0.0 )
    return image.convert('RGB', matrix)


def adjust_color_temp(img_fn, save_dir):
    image = Image.open(img_fn)
    base_name = osp.basename(img_fn)
    fn, ext = osp.splitext(base_name)

    for k in kelvin_table.keys():
        rlt_img = convert_temp(image, k)
        save_name = osp.join(save_dir, fn + '_temp' + str(k) + '.jpg')
        rlt_img.save(save_name, 'JPEG')


if __name__=='__main__':
    in_fn = ''
    save_dir = './output'

    if len(sys.argv)>1:
        in_fn = sys.argv[1]
    
    if len(sys.argv)>2:
        save_dir = sys.argv[2]

    if not osp.exists(save_dir):
        os.makedirs(save_dir)

    adjust_color_temp(in_fn, save_dir)