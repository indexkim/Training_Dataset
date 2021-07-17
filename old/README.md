# Training_Dataset_sub
- 업무 수행 주체: 본인
- 빈도: main 대비 간헐적으로 수행하며, 일회성 업무를 포함합니다.
- 부서 내 업무 지원 및 컨소시엄 내 업무 협조 요청을 포함합니다.
1. quality management
2. feedback from inspection
3. labeling_show
4. labeling_refinement_validation
5. ad-hoc analysis
6. troubleshooting



# Training_Dataset


## 학습데이터 구축 공정

- 수집 2. 정제 3. 가공 4. 검수 5. 학습의 5단계로 구성

1. 수집: 원시데이터 수집(이미지)
2. 정제: 원시데이터의 파일명 변환, 이미지 해상도 조정, 흔들린 사진 폐기, 개인정보 비식별화를 통해 원천데이터 획득
3. 가공: 원천데이터(jpg) + 어노테이션 데이터(Json) = 데이터셋 완성
4. 검수: 데이터셋 육안 검수
5. 학습: 검수를 통과한 데이터셋 학습


## 가공 공정 일일 업무

1. refinement_labeling.py: 가공 전 입고된 원천데이터 적합성 검증, DB화, 창고로 이동, 창고의 원천데이터 물량 현행화
2. labeling_distribution.py: 작업자 고용 현황, 사업 일정, 공정단계별 종별 잔여 물량 체크 후 작업물 분배, 분배 내역 DB화
3. labeling_finished.py: 분배된 작업량을 전부 업로드했는지 확인. 조건 미충족시 Slack App(Bot) 알림
4. labeling_validation.py: 일 단위 데이터 추출 > 데이터 변형(정형화) 및 필터링 > 1차 검수 > 1차 검수 결과 적합 목록 DB화, 수량 집계 및 작성, 부적합 목록은 사유별 적재
5. labeling_validation_batch.py: 1차 검수 결과 적합 목록 추출 > 검수 서버 구조에 맞게 변환 > 데이터 적재(이관) > 이관 목록 생성
6. labeling_refinement_validation.py: 1차 검수 부적합 중 정제 데이터 누락으로 부적합인 경우 보완 후 2번째 1차 검수 > ...
7. validation_labeling.py: 검수 공정 결과 부적합 사유가 가공인 경우 재작업 대상자 Slack App(Bot) 알림


## ETC

1. 요청 데이터 Ad-hoc Analysis
2. 파일 자동 생성 및 이메일 전송
3. Ground Truth 검증을 위한 viewer 개발: labeling_show_PIL.py, labeling_show_semi.py
4. 데이터 품질 관리: 육안 검수 결과 수정이 필요한 어노테이션 데이터 일괄 수정: json_dump.py
5. 필요 시 데이터 정제: rename.py resize.py
6. 프로젝트 진척사항 관리용 데이터 추출 : annotation_data_to_csv.py
7. 원천데이터(jpg) 검수: image_search_exif.py, image_search_blur.py




## 데이터셋 이름 규칙
![슬라이드3](https://user-images.githubusercontent.com/62425277/123051205-7d491580-d43c-11eb-98a7-9a483e52165f.JPG)


## 데이터셋 구조 - 라벨링 전

![슬라이드4](https://user-images.githubusercontent.com/62425277/123051270-918d1280-d43c-11eb-88a1-862abf239bc1.JPG)

## 데이터셋 구조 - 라벨링 후

![슬라이드5](https://user-images.githubusercontent.com/62425277/123051317-9ce03e00-d43c-11eb-8dd3-71dee8a261ac.JPG)


## 데이터셋 구조 - 라벨링 후_예시
![슬라이드6](https://user-images.githubusercontent.com/62425277/123051361-a9fd2d00-d43c-11eb-8f6e-c1a89535fc10.JPG)




## 정제-가공-검수 pipeline


