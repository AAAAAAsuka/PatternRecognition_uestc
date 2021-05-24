# -*- coding: utf-8 -*-
# @Time : 2021/4/27 22:53
# @Author : AsukaTelevision
# @Site : 
# @File : stitching.py
# @Software: PyCharm
# !/usr/bin/env python

'''
Stitching sample
================

Show how to use Stitcher API from python in a simple way to stitch panoramas
or scans.
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv

import argparse
import sys
import time

modes = (cv.Stitcher_PANORAMA, cv.Stitcher_SCANS)

parser = argparse.ArgumentParser(prog='stitching.py', description='Stitching sample.')
parser.add_argument('--mode', type=int, choices=modes, default=1, help='stitcher mode')
parser.add_argument('--output', default='auto', help='output picture name')
parser.add_argument('--img', default='s2.jpg,s3.jpg,s4.jpg', help='input images')
parser.add_argument('--datadir', default='data/', help='data`s loc')


def main():

    args = parser.parse_args()

    if 'auto' == args.output:
        mode_name = 'PANORAMA' if args.mode ==  0 else 'SCANS'
        args.output = f'outputs/result_{mode_name}_[{args.img}].jpg'
    args.img = args.img.split(sep=',')
    # 读取图像数据
    imgs = []
    for img_name in args.img:
        img = cv.imread(cv.samples.findFile(args.datadir + img_name))
        imgs.append(img)

    stitcher = cv.Stitcher.create(args.mode)
    since = time.time()
    status, pano = stitcher.stitch(imgs)
    end = time.time()
    if status != cv.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
        sys.exit(-1)

    cv.imwrite(args.output, pano)
    print("stitching completed successfully. %s saved!" % args.output)

    print(f'use time: {end-since}s')


if __name__ == '__main__':
    main()
    cv.destroyAllWindows()