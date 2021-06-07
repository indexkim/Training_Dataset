#!/usr/bin/env python
# coding: utf-8

import os
import glob
import numpy as np
import cv2


path = r'.'


def variance_of_laplacian(image):  
    return cv2.Laplacian(image, cv2.CV_64F).var()


threshold = 100.0
blurry = set()


for folder in sorted(os.listdir(path)):
    for file in sorted(os.listdir(path+'/'+folder)):
        if file.endswith('jpg'):
            jpg_path = path+'/'+folder+'/'+file
            image = cv2.imread(jpg_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = variance_of_laplacian(gray)
            if fm < threshold:
                blurry.add(file)

                
b_list=set()
for blur in sorted(blurry):
    b_list.add(blur[:17])
for blur2 in sorted(b_list):    
    for folder in sorted(os.listdir(path)):
        if blur2 in folder:
            os.rename(path+'/'+folder, path+'/'+folder+'_b') #_b: 흔들린 사진이라는 표시            

