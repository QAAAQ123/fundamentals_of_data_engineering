### 개념
- 한 쌍의 SQL 스크립트 실행 => 비교 연산자를 기반으로 둘을 비교하는 파이썬 스크립트
- 각 스크립트와 결과의 조합은 검증 테스트

### validator.py
- 유효성 검사기 코드
- Redshift DWH에 대한 테스트 코드 실행

##### notes
- chap 4,5,6에서 임시로 사용했던 로컬 스토리지, DuckDB 사용하지 않음
- Redshift에 연결 되어 있다고 가정하고 작성
- chap7_02_elt_pipeline_sample에 validator.py를 실행하는 task 추가
