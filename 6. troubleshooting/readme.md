# troubleshooting
1. image_search_exif
- 데이터셋의 일부 이미지가 무작위로 회전되는 문제가 발생한 적 있습니다.
EXIF data 중 Orientation의 확인을 통해 Classification with Localization Error 예상 목록을 생성합니다.
2. rename & resize: 
- 중복 데이터 관리를 위해 한번 정제된 데이터는 move로만 분배합니다. 
다만, 분배된 작업물이 작업자 실수로 삭제되는 경우가 종종 발생하는데, 이러한 경우 원시데이터 서버에서 데이터를 copy한 후, rename&resize를 거쳐 복구합니다.
