#!/usr/bin/env python
# coding: utf-8



import os
import glob
import re
import json
import shutil
import pandas as pd



#디렉토리 구조(라벨링 전): X:\TrainingData\Labeling\Team\Member\label_before\member_date_before\folder\file    
#디렉토리 구조(라벨링 후): X:\TrainingData\Labeling\Team\Member\label_after\member_date_after\folder\file    
#pathlist, freelist = X:\TrainingData\Labeling\Team\Member\label_before\member_date_before


#1. 일별 작업자 확인 및 작업폴더 생성


yyyymmdd = '20210601'
member_list =[
'A-01',
'A-02',
'A-03'
'A-04',
'A-05'

]


for member in sorted(member_list):
    for label in sorted(glob.iglob(r'X:\TrainingData\Labeling\**\**', recursive = False)):
        if member in label:
            try:
                os.mkdir(label + '\\label_before\\' + member + '_' + yyyymmdd + '_before')
                os.mkdir(label + '\\label_after\\' + member + '_' + yyyymmdd + '_after')
            except FileExistsError:
                pass

            
#2. 작업자 전원 일괄 분배


storage_path = 'C:/Users/Jisoo/Desktop/resource_data/storage'
distribute_count = 300 #일일 작업량 - 상용직은 일일 작업량이 정해져 있음
path_list = []


for member_date in sorted(glob.iglob(r'X:\TrainingData\Labeling\**\**\label_before\**', recursive = False)):
    if yyyymmdd in member_date:
        path_list.append(member_date) # 생성한 작업폴더를 분배 목록에 추가
        
for pathlist in path_list:
    while len(os.listdir(pathlist)) < distribute_count:
        for folder in sorted(os.listdir(storage_path)):
            if len(os.listdir(pathlist)) < distribute_count:
                shutil.move(storage_path + '\\' + folder, pathlist + '\\' + folder) #일일 작업량 개수만큼 폴더 이동
            else:
                break
        break

                
#3. 특정 작업자 추가 분배


freelancer_list =[
'A-01',
]


storage_path = 'C:/Users/Jisoo/Desktop/resource_data/storage'
free_list = []


for member_date in sorted(glob.iglob(r'X:\TrainingData\Labeling\**\**\label_before\**', recursive = False)):
    if yyyymmdd in member_date:
        for free in freelancer_list:
            if free in member_date:
                free_list.append(member_date)
                
for freelist in free_list:
    while len(os.listdir(freelist)) < 500 : #프리랜서는 작업량 추가 가능 - 요청 수량 직접 기재
        for folder in sorted(os.listdir(storage_path)):
            if len(os.listdir(freelist)) < 500 :
                shutil.move(storage_path + '\\' + folder, freelist + '\\' + folder) #요청 수량만큼 폴더 이동
            else:
                break
        break

        
#4. 특정 클래스 분배


storage_path = 'C:/Users/Jisoo/Desktop/resource_data/storage'
distribute_count = 300 #일일 작업량 - 상용직은 일일 작업량이 정해져 있음
path_list = []


for member_date in sorted(glob.iglob(r'X:\TrainingData\Labeling\**\**\label_before\**', recursive = False)):
    if yyyymmdd in member_date:
        path_list.append(member_date) # 생성한 작업폴더를 분배 목록에 추가
        
for pathlist in path_list:
    while len(os.listdir(pathlist)) < distribute_count:
        for folder in sorted(os.listdir(storage_path)):
            if folder[:2] == '01': #앞 2글자로 클래스 구분
                if len(os.listdir(pathlist)) < distribute_count:
                    shutil.move(storage_path + '\\' + folder, pathlist + '\\' + folder) #일일 작업량 개수만큼 폴더 이동
                else:
                    break
            break

            
#5. 특정 작업자 추가 분배 + 특정 클래스 분배 
##상기 조건 외 다양한 방식으로 변형 및 활용 가능

freelancer_list =[
'A-01',
]


storage_path = 'C:/Users/Jisoo/Desktop/resource_data/storage'
free_list = []

for member_date in sorted(glob.iglob(r'X:\TrainingData\Labeling\**\**\label_before\**', recursive = False)):
    if yyyymmdd in member_date:
        for free in freelancer_list:
            if free in member_date:
                free_list.append(member_date)
                
for freelist in free_list:
    while len(os.listdir(freelist)) < 500 : #프리랜서는 작업량 추가 가능 - 요청 수량 직접 기재하거나 변수 사용
        for folder in sorted(os.listdir(storage_path)):
            if folder[:2] == '01': #앞 2글자로 클래스 구분
                if len(os.listdir(freelist)) < 500 :
                    shutil.move(storage_path + '\\' + folder, freelist + '\\' + folder) #요청 수량만큼 폴더 이동
                else:
                    break
            break

            
#6. 해당 날짜 분배 수량 체크 - 작업자별


for pathlist in path_list:
    print(pathlist, len(os.listdir(pathlist)))
    
    
#7. 해당 날짜 분배 수량 체크 - 클래스별


count_dict = {'01':0,'02':0,'03':0,'04':0,'05':0,'06':0,'07':0,'08':0,'09':0,'10':0,'11':0,'12':0,'13':0,'14':0,'15':0,'16':0,'17':0,'18':0,
'19':0,'20':0,'21':0,'22':0,'23':0,'24':0,'25':0}


for pathlist in path_list:
    for folder in sorted(os.listdir(pathlist)):
        count_dict[folder[0:2]] += 1

        
df = pd.DataFrame.from_dict(count_dict, orient = 'index', columns = [str(yyyymmdd)+'_할당'])
print(df)
df.sum()
#label_count_xlsx = 'data/' + str(yyyymmdd) + '_label_count_.xlsx'
#df.to_excel(label_count_xlsx, sheet_name = yyyymmdd) #수량 파일


#8. 작업일자별 리스트 파일 생성 -txt, xlsx


label_list = set()
for pathlist in path_list:
    for folder in sorted(os.listdir(pathlist)):
        label_list.add(pathlist + '/' + folder)
        label_txt = 'data/' + str(yyyymmdd) + '_label_list.txt'
        with open(label_txt, 'w') as f:
            f.write('\n'.join(sorted(label_list)))

            
label_list = pd.DataFrame(sorted(label_list), columns = [yyyymmdd])
label_xlsx = 'data/' + str(yyyymmdd) + '_label_list.xlsx'
with pd.ExcelWriter(label_xlsx, engine = 'xlsxwriter') as writer:
    label_list.index = label_list.index + 1
    label_list.to_excel(writer, sheet_name = yyyymmdd)
    writer.book.use_zip64()
    writer.save()

