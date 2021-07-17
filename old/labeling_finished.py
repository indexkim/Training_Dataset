#!/usr/bin/env python
# coding: utf-8



import os
import glob
import requests
import schedule



yyyymmdd = '20210601'

member_id = ['A-01:<@U0123456789|cal>', #작업자 태그용 Slack Id 
'A-02:<@U1234567890|cal>'             
]


def rework_message():
    def post_message(token, channel, text):
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization" : "Bearer"+ token},
            data={"channel" : channel, "text" : text}
        )
        print(response)

    myToken = "my-slack-token-000000000000000000000000"    #Slack Api  - Bot User OAuth Token 


    path_list_before=[]
    for member_date in sorted(glob.iglob(r'X:\TrainingData\Labeling\**\**\label_before\**', recursive = False)):
        if yyyymmdd in member_date:
            path_list_before.append(member_date)

    path_list_after=[]
    for member_date in sorted(glob.iglob(r'X:\TrainingData\Labeling\**\**\label_after\**', recursive = False)):
        if yyyymmdd in member_date:
            path_list_after.append(member_date)



    #재작업 폴더 알림
    p_list_after = set()
    rework_list = set()
    for pathlist_a in path_list_after:
        uploaded_cnt = 0 
        rework_cnt = 0
        for folder in sorted(os.listdir(pathlist_a)):
            uploaded_cnt += 1
            p_list_after.add(folder[:17])
            jpg_cnt = 0
            json_cnt = 0
            for file in sorted(os.listdir(pathlist_a+'/'+folder)):
                if file.endswith('jpg'):
                    jpg_cnt += 1
                elif file.endswith('Json'):
                    json_cnt += 1
            if json_cnt != jpg_cnt :
                rework_cnt += 1
                rework_list.add(folder)
            if folder in rework_list:
                for m in member_id :
                    if m[:4] == pathlist_a[-19:-15]: #해당 작업자 태그 및 내용 전송
                        post_message(myToken, "#rework_notice", m[5:]+'님,'+yyyymmdd+'일 작업물 중 재작업 대상 폴더가 있습니다. '+str(rework_cnt)+'.'+folder)

    #미업로드 폴더 알림
    for pathlist_b in path_list_before:
        distributed_cnt = 0    
        missed_cnt = 0
        for folder in sorted(os.listdir(pathlist_b)):
            distributed_cnt += 1
            if folder in p_list_after:
                pass
            else:
                missed_cnt += 1
                m_cnt = len(os.listdir(pathlist_b)) - uploaded_cnt
                for m in member_id :
                    if m[:4] == pathlist_b[-20:-16]: #해당 작업자 태그 및 내용 전송
                        post_message(myToken, "#rework_notice", m[5:]+'님,'+yyyymmdd+'일 작업량 '+str(len(os.listdir(pathlist_b)))+'개 중 '+str(m_cnt)+'개가 업로드되지 않았습니다. '+str(missed_cnt)+'. '+folder)

                        
                        
    #관리자용 채널에 작업자별 작업 내역 전송             
    post_message(myToken, "#labeling_admin", pathlist_a[-19:]+'/분배개수:'+str(distributed_cnt)+'/업로드개수:'+str(uploaded_cnt)+'/미업로드개수:'+str(m_cnt)+'/재작업개수:'+str(rework_cnt))        

    

schedule.every().days.at("09:30").do(rework_message)  #매일 오전 9시 30분 작동


while True: 
    schedule.run_pending() 
    time.sleep(1)

