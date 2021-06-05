#!/usr/bin/env python
# coding: utf-8



import os
import json
import glob
import argparse
import numpy as np
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from collections import defaultdict




# 특정 EXIF 정보 추출

path = r'.'

def exif_search(path, folder, file, image):
    jpg_path = path+'/'+folder+'/'+file
    image = Image.open(jpg_path)
    exif = image._getexif();
    image.close()
    print(file, exif[36867]) #36867: DateTimeOriginal
            

for folder in sorted(os.listdir(path)):
    for file in sorted(os.listdir(path+'/'+folder)):
        if file.endswith('jpg'):
             exif_search(path, folder, file, image)
            
            
            
# 회전(Orientation) 여부 : 회전된 경우에만 Orientation이 EXIFTAGS의 Key로 존재

path = r'.'

def exif_or_not(path, folder, file, image):
    jpg_path = path+'/'+folder+'/'+file
    try:
        image = Image.open(jpg_path)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())
        print(jpg_path, exif[274])

    except (AttributeError, KeyError, IndexError):
        print(jpg_path, 'No Orientation')
        pass


for folder in sorted(os.listdir(path)):
    for file in sorted(os.listdir(path+'/'+folder)):
        if file.endswith('jpg'):
             exif_or_not(path, folder, file, image)
                



                
#36864: ExifVersion
#37377: ShutterSpeedValue
#37378: ApertureValue
#36867: DateTimeOriginal
#36868: DateTimeDigitized
#37379: BrightnessValue
#37380: ExposureBiasValue
#37381: MaxApertureValue
#37383: MeteringMode
#37385: Flash
#37386: FocalLength
#40961: ColorSpace
#40962: ExifImageWidth
#41988: DigitalZoomRatio
#41989: FocalLengthIn35mmFilm
#41990: SceneCaptureType
#40963: ExifImageHeight
#256: ImageWidth
#257: ImageLength
#271: Make
#272: Model
#531: YCbCrPositioning
#282: XResolution
#283: YResolution
#41729: SceneType
#42016: ImageUniqueID
#34850: ExposureProgram
#34853: GPSInfo
#34855: ISOSpeedRatings
#296: ResolutionUnit
#41986: ExposureMode
#41987: WhiteBalance
#305: Software
#306: DateTime
#34665: ExifOffset
#33434: ExposureTime
#33437: FNumber
#274: Orientation

