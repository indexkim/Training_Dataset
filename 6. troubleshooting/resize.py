#!/usr/bin/env python
# coding: utf-8



import os
import glob
import json
import argparse
import numpy as np
from PIL import Image, ExifTags
import piexif
from collections import defaultdict


DEFAULT_MAX_SIZE = 1921
DEFAULT_MIN_SIZE = 1081
DEFAULT_SRC_DIR = 'C:\\Users\\Jisoo\\Desktop\\resizing'
resolution = []


def count_resolution(width, height):
    flag = False
    for i in range(len(resolution)):
        if resolution[i][0] == width and resolution[i][1] == height:
            flag = True
            resolution[i][2] = resolution[i][2] + 1
            break

    if flag == False:
        resolution.append([width, height, 1])


def change_size_image(maxSize, minSize, fname):
    try:
        try:
            img = Image.open(fname)
        except:
            fpLog.write('File Open Error: ' + fname + '\\\\n')
            return

        try:
            exif_dict = piexif.load(img.info['exif'])
            del exif_dict['thumbnail']
            del exif_dict['1st']
        except KeyError:
            exif_dict = defaultdict(dict)

        nimg = np.array(img)
        height, width, _ = nimg.shape
        count_resolution(width, height)
        maxLength = max(width, height)
        ratio = maxSize / maxLength
        if ratio * width < minSize or ratio * height < minSize:
            minLength = min(width, height)
            ratio = minSize / minLength
        width = int(width * ratio)
        height = int(height * ratio)
        rimg = img.resize((width, height))
        # ValueError: "dump" got wrong type of exif value
        exif_dict['Exif'][41729] = b'1'
        exif_bytes = piexif.dump(exif_dict)
        rimg.save(fname, exif=exif_bytes)
    except:
        return


def get_size(resolution):
    i = resolution.find('*')
    width = int(resolution[0:i])
    height = int(resolution[(i+1):len(resolution)])
    return (width, height)


def change_size_json(maxSize, minSize, fname):
    try:
        jfile = open(fname, 'rt', encoding='UTF-8')
        jdata = json.load(jfile)
        jfile.close()
        width, height = get_size(jdata['RESOLUTION'])
        maxLength = max(width, height)
        ratio = maxSize / maxLength
        if ratio * width < minSize or ratio * height < minSize:
            minLength = min(width, height)
            ratio = minSize / minLength
        width = int(width * ratio)
        height = int(height * ratio)
        jdata['RESOLUTION'] = str(width)+'*'+str(height)

        for i in range(int(jdata['BoundingCount'])):
            x1 = int(jdata['Bounding'][i]['x1'])
            jdata['Bounding'][i]['x1'] = str(int(x1 * ratio))
            y1 = int(jdata['Bounding'][i]['y1'])
            jdata['Bounding'][i]['y1'] = str(int(y1 * ratio))
            x2 = int(jdata['Bounding'][i]['x2'])
            jdata['Bounding'][i]['x2'] = str(int(x2 * ratio))
            y2 = int(jdata['Bounding'][i]['y2'])
            jdata['Bounding'][i]['y2'] = str(int(y2 * ratio))

        jfile = open(fname, 'wt', encoding='UTF-8')
        json.dump(jdata, jfile, indent=2, ensure_ascii=False)
        jfile.close()
    except:
        return


def change_size(dirName, maxSize, minSize):
    files = glob.glob(os.path.join(dirName, '*'))
    for fname in files:
        if os.path.isdir(fname):
            change_size(fname, maxSize, minSize)
            continue
        print(fname)
        bname = os.path.basename(fname)
        sname = os.path.splitext(bname)
        if sname[1] == '.Json':
            change_size_json(maxSize, minSize, fname)
        elif sname[1] == '.jpg':
            change_size_image(maxSize, minSize, fname)


change_size(DEFAULT_SRC_DIR, DEFAULT_MAX_SIZE, DEFAULT_MIN_SIZE)


