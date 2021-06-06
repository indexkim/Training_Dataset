# Training_Dataset

## 수집(Acquisition) - 정제(Refinement) - 가공(Labeling) - 검수(Validation) - 학습(Training)


1. Refinement - Labeling : 가공 전 정제 데이터(jpg) 적합성 검증
2. Labeling : 데이터 라벨러 작업물 분배, 작업 실적, 근태 관리 등 가공단 내부 공정 업무 전반
3. Labeling - Validation : 가공 후 데이터 세트(jpg+Json) 적합성 검증 및 분류별 집계 == 1차 검수
4. Labeling - Validation - Batch : 1차 검수를 통과한 데이터 세트를 2차 검수 기관으로 이관
5. Labeling - Refinement - Validation : Labeling - Validation에서 필수값 누락으로 부적합인 경우, 필수값 입력 후 적합성 재검증
6. Labeling - Refinement - Validation : Labeling - Refinement - Validation에서 적합성 재검증된 데이터 세트를 2차 검수 기관으로 이관
7. Validation - Labeling : 2차 검수 피드백 결과 재가공이 필요한 경우 해당 라벨러에게 재작업 안내
8. Validation - Refinement : 2차 검수 피드백 결과 재수집, 재정제가 필요한 경우 수집, 정제 담당자에게 부적합 목록 전송



## 대분류(PROJECT SORTING)/중분류(CLASS)/소분류(DETAILS)

1. 대분류01 / 중분류 01-10 / 소분류
2. 대분류02 / 중분류 11-25 / 소분류




/labeler_yyyymmdd/folder/file



## dataset
00_X000_C000_mmdd
00_X000_C000_mmdd_0.jpg
00_X000_C000_mmdd_0.Json
