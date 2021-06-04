#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import glob
import pandas as pd
import json
import shutil



yyyymmdd = '20210601'


# fastcopy

def _copyfileobj_faster(fsrc, fdst, length = 16 * 1024 * 1024):
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)

shutil.copyfileobj = _copyfileobj_faster




class_dict ={ # 01번부터 25번까지 총 25가지의 클래스가 있으며, 클래스별로 상세항목이 존재한다. 여기서는 간략히 표시한다.
    
    '01':['a','b','c','d','e'],
    '02':['aa','bb','cc','dd','ee'],
    '03':['aaa','bbb','ccc','ddd','eee'],
    ...
    '25':['aaaaa','bbbbb','ccccc','ddddd','eeeee']
        
}

# 이관 경로 설정


path1 = 'E:/ProjectSorting01' #ProjectSorting01(대분류)경로 
path2 = 'E:/ProjectSorting02' #ProjectSorting02(대분류)경로


b1 = len(os.listdir(path1))
b2 = len(os.listdir(path2))


c1 = 'E:/ProjectSorting01/batch_'+'%0.3d'%+int(b1+1)+'_doing' # 경로상의 폴더수+1 로 batch naming. batch_009 까지 있으면 batch_010 생성
c2 = 'E:/ProjectSorting02/batch_'+'%0.3d'%+int(b2+1)+'_doing' # doing : 업로드중이니 다운로드 불가능


copy_dict={
    
    '01' : c1+'/01/',
    '02' : c1+'/02/',
    '03' : c1+'/03/',
    '04' : c1+'/04/',
    '05' : c1+'/05/',
    '06' : c1+'/06/',
    '07' : c1+'/07/',
    '08' : c1+'/08/',
    '09' : c1+'/09/',
    '10' : c1+'/10/',
    '11' : c2+'/11/',
    '12' : c2+'/12/',
    '13' : c2+'/13/',
    '14' : c2+'/14/',
    '15' : c2+'/15/',
    '16' : c2+'/16/',
    '17' : c2+'/17/',
    '18' : c2+'/18/',
    '19' : c2+'/19/',
    '20' : c2+'/20/',
    '21' : c2+'/21/',
    '22' : c2+'/22/',
    '23' : c2+'/23/',
    '24' : c2+'/24/',
    '25' : c2+'/25/'
}


path_list_after = []
for member_date in sorted(glob.iglob(r'X:\TrainingData\Labeling\**\**\label_after\**', recursive = False)):
    if yyyymmdd in member_date:
        path_list_after.append(member_date)


batch_list = set()
for pathlist_a in path_list_after:
    for folder in sorted(os.listdir(pathlist_a)):
        if re.findall(r'^[0-2][0-9]_X[0-9][0-9][0-9]_C[0-9][0-9][0-9]_[0-1][0-9][0-3][0-9]$', folder):
            jpg_cnt = 0
            json_cnt = 0
            for file in sorted(os.listdir(pathlist_a+'/'+folder)):
                if file.endswith('Json'):
                    json_path = pathlist_a +'/'+ folder+'/'+ file
                    jfile = open(json_path, 'rt', encoding = 'UTF-8')
                    jdata = json.load(jfile)            
                    jfile.close()
                    bound_cnt = int(jdata['BoundingCount'])
                    for i in range(1):
                        if len(jdata['GPS']) < 5: #주로 누락되는 필수값1
                            gps.add(pathlist_a+'/'+folder)
                            pass
                        elif len(jdata['Aperture values']) < 1: #주로 누락되는 필수값2
                            aper.add(pathlist_a+'/'+folder)
                            pass
                        elif jdata['Bounding'][i]['DETAILS'] not in class_dict[folder[:2]]: # 01_a는 맞지만, 02_a는 틀림
                            classdetail.add(pathlist_a+'/'+folder)
                            pass
                        else:
                            json_cnt += 1 # 상기 조건을 전부 만족해야 적합으로 간주
                elif file.endswith('jpg'):
                    jpg_cnt += 1
            if jpg_cnt != json_cnt:
                pass
            else:
                try:
                    print(pathlist_a+'/'+folder+'/'+file, copy_dict[folder[:2]]+folder+'/'+file)
                    shutil.copytree(pathlist_a+'/'+folder, copy_dict[folder[:2]]+folder)
                    batch_list.add(pathlist_a+'/'+folder+', '+copy_dict[folder[:2]]+folder)
                except FileExistsError:
                    pass
                except FileNotFoundError:
                    pass                            
 
                            


batch_list = pd.DataFrame(batch_list, columns = [str(yyyymmdd)+'_batch_list'])                            
batch_list_xlsx = 'data/batch/' + str(yyyymmdd) + '_batch_list.xlsx'


with pd.ExcelWriter(batch_list_xlsx, engine = 'xlsxwriter') as writer:
    batch_list.index = batch_list.index + 1
    batch_list.to_excel(writer, sheet_name = str(yyyymmdd)+'_batch_list')
    writer.book.use_zip64()
    writer.save()



# 1차 검수 완료 및 이관 목록 2차 검수 담당자 이메일로 자동 전송


import smtplib 
from email import encoders  
from email.mime.text import MIMEText   
from email.mime.multipart import MIMEMultipart   
from email.mime.base import MIMEBase 


smtp = smtplib.SMTP('smtp.gmail.com', 587) 
smtp.ehlo()
smtp.starttls()   
smtp.login('mymail@gmail.com', 'mypassword')


validation_mail = ['validation_mail@gmail.com'] #2차 검수 담당자 메일 주소
msg = MIMEMultipart()
msg['Subject'] = str(yyyymmdd)+'_일자 batch' #제목
part = MIMEText(str(yyyymmdd)+'일자 batch 목록입니다.' )  #내용
msg.attach(part)


filepath = batch_list_xlsx


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

    
# 전송 완료 - doing 제거 및 다운로드 허용


os.rename(c1, c1[:-6])
os.rename(c2, c2[:-6])


#모든 작업 완료 시 알림 전용 slack 채널로 알림


import requests

def post_message(token, channel, text):
    response = requests.post('https://slack.com/api/chat.postMessage',
        headers={'Authorization' : 'Bearer'+ token},
        data={'channel' : channel, 'text' : text}
    )
    print(response)

myToken = 'my-slack-token-000000000000000000000000'    #Slack Api  - Bot User OAuth Token 

post_message(myToken,'#notice_me', str(yyyymmdd) +'_'+c1[-15:-6]+'_'+c2[-15:-6]+'_전송완료') #작업완료 알림 채널에 완료 메시지 전송

