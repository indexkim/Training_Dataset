#!/usr/bin/env python
# coding: utf-8



import os
import glob
import json
import pandas as pd


def annotation_data(path, folder, file, json_path, cnt):
    jfile = open(json_path, 'rt', encoding='UTF-8')
    jdata = json.load(jfile)
    jfile.close()
    json_name = file
    jpg_name = jdata['FILE NAME']
    json_path = path+'/'+folder+'/'+file
    jpg_path = path+'/'+folder+'/'+jdata['FILE NAME']
    collection_method = jdata['COLLECTION METHOD']
    form = jdata['FORM']
    date = jdata['DATE']
    gps = jdata['GPS']
    id_code = jdata['ID CODE']
    resolution = jdata['RESOLUTION']
    focus_distance = jdata['focus distance']
    exposure_time = jdata['exposure time']
    aperture_values = jdata['Aperture values']
    sensitivity_iso = jdata['Sensitivity iso']
    exposure_method = jdata['exposure method']
    make = jdata['MAKE']
    camera_model_name = jdata['Camera Model Name']
    software = jdata['Software']
    file_size = jdata['File Size']
    day_night = jdata['DAY/NIGHT']
    place = jdata['PLACE']
    project_sorting = jdata['PROJECT SORTING']
    b_count = jdata['BoundingCount']
    b_class_list=[]
    b_details_list = []
    b_damage_list = []
    b_transparency_list = []
    b_color_list = []
    b_shape_list = []
    b_material_list = []
    b_object_size_list = []
    b_direction_list = []
    b_drawing_list = []
    b_box_list = []
    b_polygon_list = []


    for i in range(int(b_count)):
        b_class_list.append(jdata['Bounding'][i]['CLASS'])
        b_details_list.append(jdata['Bounding'][i]['DETAILS'])
        b_damage_list.append(jdata['Bounding'][i]['DAMAGE'])
        b_transparency_list.append(jdata['Bounding'][i]['TRANSPARENCY'])
        b_color_list.append(jdata['Bounding'][i]['Color'])
        b_shape_list.append(jdata['Bounding'][i]['Shape'])
        try:
            b_material_list.append(jdata['Bounding'][i]['Material'])
        except KeyError:
            pass
        try:
            b_material_list.append(jdata['Bounding'][i]['Texture'])
        except KeyError:
            pass
        b_object_size_list.append(jdata['Bounding'][i]['Object Size'])
        b_direction_list.append(jdata['Bounding'][i]['Direction'])
        b_drawing_list.append(jdata['Bounding'][i]['Drawing'])        
        if jdata['Bounding'][i]['Drawing'] == 'BOX':
            b_box_list.append((jdata['Bounding'][i]['x1'], jdata['Bounding'][i]['y1'], jdata['Bounding'][i]['x2'], jdata['Bounding'][i]['y2']))
        elif jdata['Bounding'][i]['Drawing'] == 'POLYGON':
            point_cnt = int(jdata['Bounding'][i]['PolygonCount'])
            for k in range(point_cnt):
                a = list(jdata['Bounding'][i]['PolygonPoint'][k].values())
                x,y = int(a[0].split(',')[0]),int(a[0].split(',')[1])
                b_polygon_list.append([x, y])


            

    df.loc[cnt]=[json_name,json_path,jpg_name,collection_method,form,date,gps,id_code,resolution,focus_distance,
                 exposure_time,aperture_values,sensitivity_iso,exposure_method,
                 make,camera_model_name,software,file_size,day_night,place,project_sorting,
                 b_count,b_class_list,b_details_list,b_damage_list,b_transparency_list,b_color_list,b_shape_list,
                 b_material_list,b_object_size_list,b_direction_list,b_drawing_list,b_box_list,b_polygon_list]




cnt = 0
df = pd.DataFrame(columns=['JSON_NAME','FILE_PATH','FILE_NAME','COLLECTION_METHOD','FORM','DATE','GPS','ID_CODE',
                          'RESOLUTION','FOCUS_DISTANCE','EXPOSURE_TIME','APERTURE_VALUES','SENSITIVITY_ISO','EXPOSURE_METHOD',
                          'MAKE','CAMERA_MODEL_NAME','SOFTWARE','FILE_SIZE','DAY_NIGHT','PLACE','PROJECT_SORTING',
                          'BOUNDING_COUNT','BOUNDING_CLASS','BOUNDING_DETAILS','BOUNDING_DAMAGE','BOUNDING_TRANSPARENCY',
                           'BOUNDING_COLOR','BOUNDING_SHAPE','BOUNDING_MATERIAL','BOUNDING_OBJECTSIZE','BOUNDING_DIRECTION',
                           'BOUNDING_DRAWING','BOUNDING_BOX','BOUNDING_POLYGON'
])


path = r'.'
for folder in sorted(os.listdir(path)):
    for file in sorted(os.listdir(path+'/'+folder)):
        if file.endswith('Json'):
            json_path = path+'/'+folder+'/'+file
            annotation_data(path, folder, file, json_path, cnt)
            cnt += 1

            
df.to_csv('data/annotation.csv', encoding='UTF-8-sig')

