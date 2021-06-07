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
is_N0 = df['불사유'].isin(['N0','N5','N6','N7']) # 부적합 사유: 수집 및 정제 오류
N0 = df[is_N0]
val_return_list = set(N0.iloc[:,7] + N0.iloc[:,18]) #파일


validation_feedback_refinement = pd.DataFrame(val_return_list, columns = [str(yyyymmdd)+'_validation_feedback_refinement'])           
validation_feedback_refinement_xlsx = 'data/validation_feedback_refinement/' + str(yyyymmdd) + '_validation_feedback_refinement.xlsx'
with pd.ExcelWriter(validation_feedback_refinement_xlsx, engine = 'xlsxwriter') as writer:
    validation_feedback_refinement.index = validation_feedback_refinement.index + 1
    validation_feedback_refinement.to_excel(writer, sheet_name = str(yyyymmdd)+'_validation_feedback_refinement')
    writer.book.use_zip64()
    writer.save()

    

import smtplib 
from email import encoders  
from email.mime.text import MIMEText   
from email.mime.multipart import MIMEMultipart   
from email.mime.base import MIMEBase 


smtp = smtplib.SMTP('smtp.gmail.com', 587) 
smtp.ehlo()
smtp.starttls()   
smtp.login('mymail@gmail.com', 'mypassword')


validation_mail = ['acquisition_mail@gmail.com', 'refinement_mail@gmail.com'] #수집/정제 담당자 메일 주소
msg = MIMEMultipart()
msg['Subject'] = str(yyyymmdd)+'_일자 검수 피드백_수집정제오류' #제목
part = MIMEText(str(yyyymmdd)+'일자 검수 피드백_수집정제오류 목록입니다.' )  #내용
msg.attach(part)


filepath = validation_feedback_refinement_xlsx


with open(filepath, 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())    
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment', filename = filepath)
    msg.attach(part)
msg  

for address in validation_mail:
    msg['To'] = address
    smtp.sendmail('mymail@gmail.com', address, msg.as_string())
    print(address)

    


#모든 작업 완료 시 알림 전용 slack 채널로 알림

def post_message(token, channel, text):
    response = requests.post('https://slack.com/api/chat.postMessage',
        headers = {'Authorization' : 'Bearer'+ token},
        data = {'channel' : channel, 'text' : text}
    )
    print(response)

myToken = 'my-slack-token-000000000000000000000000'    #Slack Api  - Bot User OAuth Token 

post_message(myToken, '#notice_me', str(yyyymmdd) +'일자 검수 피드백_수집정제오류 전송 완료') #작업완료 알림 채널에 완료 메시지 전송

