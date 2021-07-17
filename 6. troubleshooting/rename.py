#!/usr/bin/env python
# coding: utf-8



#rename_dataset
import os
import glob
import json
from PIL import Image, ExifTags


path = 'C:\\Users\\Jisoo\\Desktop\\test\\01' # \ > \\ 


def find_img(path):
    files = glob.glob(os.path.join(path, '*'))
    for fname in files:
        if os.path.isdir(fname):
            find_img(fname)
            continue
        bname = os.path.basename(fname)
        sname = os.path.splitext(bname)
        if sname[1] == '.Json':
            global img_path 
            global json_path
            global img_file
            global json_file
            img_path = fname.replace('Json','jpg')
            json_path = fname
            img_file = bname.replace('Json','jpg')
            json_file = bname
            change_name()
        else:
            pass
        
        
def change_name():
    path_list = img_path.split('\\')[:-1]
    folder_path = ('\\').join(path_list)
    folder = path_list[-1]
    cnt = 999
    for file in sorted(os.listdir(folder_path)):
        if file.endswith('jpg') or file.endswith('JPG'):
            os.rename(folder_path+'/'+file, folder_path+'/'+folder+'_'+str(cnt)+'.jpg')
            try:
                os.rename(folder_path+'/'+file[:-4]+'.Json', folder_path+'/'+folder+'_'+str(cnt)+'.Json')
            except:
                pass
            cnt += 1
    cnt = 0
    for file in sorted(os.listdir(folder_path)):
        if file.endswith('jpg') or file.endswith('JPG'):
            os.rename(folder_path+'/'+file, folder_path+'/'+folder+'_'+str(cnt)+'.jpg')
            try:
                os.rename(folder_path+'/'+file[:-4]+'.Json', folder_path+'/'+folder+'_'+str(cnt)+'.Json')
            except:
                pass
            cnt += 1
    change_name_json()

    
def change_name_json():
    jfile = open(json_path, 'rt', encoding = 'UTF-8')
    jdata = json.load(jfile)
    jfile.close()
    jdata['FILE NAME'] = img_file
    jfile = open(json_path, 'wt', encoding = 'UTF-8')
    json.dump(jdata, jfile, indent = 2, ensure_ascii = False)
    jfile.close()

    
find_img(path)


#rename_image_only
import os
import glob

for path in glob.glob(r'C:\Users\Jisoo\Desktop\resizing'):
    for folder in sorted(os.listdir(path)):
        cnt=-1
        for file in sorted(os.listdir(path+'/'+folder)):
            cnt+=1
            os.rename(path+'/'+folder+'/'+file, path+'/'+folder+'/'+folder+'_'+str(cnt)+'.jpg')

