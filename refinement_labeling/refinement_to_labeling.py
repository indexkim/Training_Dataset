#!/usr/bin/env python
# coding: utf-8



import os
import pandas as pd

df = pd.read_excel('data/refine_storage.xlsx')

path = 'C:/Users/Jisoo/Desktop/resource_data/refine' # 정제 검수 대기중인 원천데이터 경로
refine_list = set()
refine_path_list = set()

for keyword in sorted(os.listdir(path)):
    if 'keyword' in keyword:            # 적합 리스트 검색 조건 입력
        for folder in sorted(os.listdir(path+'/'+keyword)):
            refine_list.add(folder)
            refine_path_list.add(path+'/'+keyword+'/'+folder)

#정제 검수결과 적합 리스트 생성 - 최초 리스트
refine_list = pd.DataFrame(refine_list, columns = ['folder'])
refine_path_list = pd.DataFrame(refine_path_list, columns = ['path'])
           
with pd.ExcelWriter('data/refine_storage.xlsx', engine='xlsxwriter') as writer:
    refine_list.index = refine_list.index + 1
    refine_list.to_excel(writer, sheet_name = 'refine_list')
    refine_path_list.index = refine_path_list.index + 1
    refine_path_list.to_excel(writer, sheet_name = 'refine_path_list')
    writer.book.use_zip64()
    writer.save()



import re
import shutil


path = 'C:/Users/Jisoo/Desktop/resource_data/refine' # 정제 검수 대기중인 원천데이터 경로
storage_path = 'C:/Users/Jisoo/Desktop/resource_data/storage' # 정제 검수 완료, 라벨링 대기
name_path = 'C:/Users/Jisoo/Desktop/resource_data/name' # 네이밍룰 에러 
same_path = 'C:/Users/Jisoo/Desktop/resource_data/same' # 중복

# 생성된 최초 리스트 불러오기 - 중복 검사용

df1 = pd.read_excel('data/refine_storage.xlsx', sheet_name = 'refine_list')
refine_list = [df1.iloc[row,1] for row in range(len(df1))] #중복 폴더 

df2 = pd.read_excel('data/refine_storage.xlsx', sheet_name = 'refine_path_list')
refine_path_list = [df2.iloc[row,1] for row in range(len(df2))] #중복 폴더 경로 

name_error = set()
same_error = set()

for folder in sorted(os.listdir(path)):
    if re.findall(r'^[0-2][0-9]_X[0-9][0-9][0-9]_C[0-9][0-9][0-9]_[0-1][0-9][0-3][0-9]$', folder):
        jpg_cnt = 0
        for file in sorted(os.listdir(path+'/'+folder)):
            if re.findall(r'^[0-2][0-9]_X[0-9][0-9][0-9]_C[0-9][0-9][0-9]_[0-1][0-9][0-3][0-9]_[0-9].jpg$', file):
                jpg_cnt += 1                
            else:
                try:
                    name_error.add(name_path+'/'+folder)
                    print(path+'/'+folder, name_path+'/'+folder) 
                    shutil.move(path+'/'+folder, name_path+'/'+folder) #네이밍룰 에러 - 파일 단위
                except FileNotFoundError:
                    pass               
    else:
        try:
            name_error.add(name_path+'/'+folder)
            print(path+'/'+folder, name_path+'/'+folder) 
            shutil.move(path+'/'+folder, name_path+'/'+folder) #네이밍룰 에러 - 폴더 단위
        except FileNotFoundError:
            pass


for folder in sorted(os.listdir(path)):        
    if len(os.listdir(path+'/'+folder)) == jpg_cnt: 
        if folder in refine_list:
            try:
                same_error.add(same_path+'/'+folder)  
                print(path+'/'+folder, same_path+'/'+folder)        
                shutil.move(path+'/'+folder, same_path+'/'+folder) # 중복 검사 
            except FileNotFoundError:
                pass

        elif folder not in refine_list:
            try:
                refine_list.append(folder)
                refine_path_list.append(path+'/'+folder) 
                print(path+'/'+folder, storage_path+'/'+folder)
                shutil.move(path+'/'+folder, storage_path+'/'+folder) # 정제 검수 통과 - 목록 추가 및 적합 창고 이동
            except FileNotFoundError:
                pass

            
            
#정제 검수결과 적합 리스트 생성 (누적)

refine_list = pd.DataFrame(refine_list, columns = ['folder'])
refine_path_list = pd.DataFrame(refine_path_list, columns = ['path'])
           
with pd.ExcelWriter('data/refine_storage.xlsx', engine = 'xlsxwriter') as writer:
    refine_list.index = refine_list.index + 1
    refine_list.to_excel(writer, sheet_name = 'refine_list')
    refine_path_list.index = refine_path_list.index + 1
    refine_path_list.to_excel(writer, sheet_name = 'refine_path_list')
    writer.book.use_zip64()
    writer.save() 

    
    
#정제 검수결과 부적합 리스트 생성(일자별)

yyyymmdd = 20210603

name_error = pd.DataFrame(name_error, columns = [str(yyyymmdd)+'_name'])
same_error = pd.DataFrame(same_error, columns = [str(yyyymmdd)+'_same'])
error_xlsx = 'data/'+str(yyyymmdd)+'_error_list.xlsx'

with pd.ExcelWriter(error_xlsx, engine = 'xlsxwriter') as writer:
    name_error.index = name_error.index + 1
    name_error.to_excel(writer, sheet_name = 'name_error')
    same_error.index = same_error.index + 1
    same_error.to_excel(writer, sheet_name = 'same_error')
    writer.book.use_zip64()
    writer.save()


#부적합 리스트 엑셀 파일 정제 담당자 이메일 자동 전송

import smtplib 
from email import encoders  
from email.mime.text import MIMEText   
from email.mime.multipart import MIMEMultipart   
from email.mime.base import MIMEBase 


smtp = smtplib.SMTP('smtp.gmail.com', 587) 
smtp.ehlo()
smtp.starttls()   
smtp.login('mymail@gmail.com', 'mypassword')


refine_mail = ['yourmail@gmail.com'] #정제 담당자 메일 주소
msg = MIMEMultipart()
msg['Subject'] = str(yyyymmdd)+'_정제 부적합' #제목
part = MIMEText(str(yyyymmdd)+'일자 정제 부적합 폴더 목록입니다.' )  #내용
msg.attach(part)

filepath = error_xlsx

with open(filepath, 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())    
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment', filename = filepath)
    msg.attach(part)
msg  

for address in refine_mail:
    msg['To'] = address
    smtp.sendmail('mymail@gmail.com', address, msg.as_string())
    print(address)   







