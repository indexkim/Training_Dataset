#!/usr/bin/env python
# coding: utf-8



import os
import glob
import re
import json
import requests
import schedule 
import time 
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import xlsxwriter


yyyymmdd = '20210601'


validation_feedback = []
for file in sorted(glob.glob("F:/**/*.xlsx")): # F:/validation/20210601_validation_feedback.xlsx'
    if yyyymmdd in file and 'xlsx' in file:
        data = pd.read_excel(file)    
        validation_feedback.append(data)
validation_feedback = pd.concat(validation_feedback)    


df = pd.DataFrame(validation_feedback)
is_N1 = df['불사유'].isin(['N1','N2','N3','N4','N8','N9']) # 부적합 사유: 가공 오류
N1 = df[is_N1]
val_return_list = set(N1.iloc[:,7] + N1.iloc[:,18]) 

    
member_id = ['A-01:<@U0123456789|cal>', #작업자 태그용 Slack Id 
'A-02:<@U1234567890|cal>'             
]


def post_message(token, channel, text):
    response = requests.post('https://slack.com/api/chat.postMessage',
        headers = {'Authorization' : 'Bearer'+ token},
        data = {'channel' : channel, 'text' : text}
    )
    print(response)

myToken = 'my-slack-token-000000000000000000000000'    #Slack Api  - Bot User OAuth Token 

  
path_list_after = []
for member_date in sorted(glob.iglob(r'D:\TrainingData\Labeling\**\**\label_after\**', recursive = False)):
    if yyyymmdd in member_date:
        path_list_after.append(member_date)


for pathlist_a in path_list_after:
    for folder in sorted(os.listdir(pathlist_a)):
        for val in val_return_list:
            if folder == val[:17]:
                rework_cnt = 0
                for file in sorted(os.listdir(pathlist_a+'/'+folder)):
                    rework_cnt+=1
                    for m in member_id:                        
                        if m[:4] == pathlist_a[-19:-15]:
                            post_message(myToken, "#rework_notice_2", m[5:]+'님,'+yyyymmdd+'일 작업물 검수 결과 부적합이므로 재작업 부탁드립니다. '+str(rework_cnt)+'.'+folder)
                            
                            
                            
                            
validation_feedback_labeling = pd.DataFrame(val_return_list, columns = [str(yyyymmdd)+'_validation_feedback_labeling'])           
validation_feedback_labeling_xlsx = 'data/validation_feedback_labeling/' + str(yyyymmdd) + '_validation_feedback_labeling.xlsx'


with pd.ExcelWriter(validation_feedback_labeling_xlsx, engine = 'xlsxwriter') as writer:
    validation_feedback_labeling.index = validation_feedback_labeling.index + 1
    validation_feedback_labeling.to_excel(writer, sheet_name = str(yyyymmdd)+'_validation_feedback_labeling')
    writer.book.use_zip64()
    writer.save()  
    
post_message(myToken, '#notice_me', str(yyyymmdd) +'일자 검수 피드백_가공오류 안내 완료') #작업완료 알림 채널에 완료 메시지 전송    

