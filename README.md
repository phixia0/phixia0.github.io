# TH QA LAB — QA 포트폴리오 v4

GitHub Pages 정적 웹사이트. GitHub 사용자명: `phixia0`.

## 내용
- `projects/login-qa/`: 로그인 기능 QA — 요구사항 분석 12건, 수동 TC 43건(43 PASS 기록), 원본 산출물 4종 및 웹 탐색기
- `projects/login-automation/`: Python + Selenium — 자동화 TC 34건(Validation 25 / Authentication 9) 및 실행 스크린샷
- `projects/login-automation/sources/`: 자동화 Python 코드 2종, CSV 2종, 묶음 ZIP
- `projects/login-automation/media/`: 제출된 실행 과정·결과 화면 4장

## 공개 주의
- `.local_secret`, `qa_practice.db` 및 로컬 상태 파일은 포함하지 않았습니다.
- CSV와 원본 산출물의 테스트용 ID/비밀번호는 가상 예시 데이터이며 실제 비밀번호로 사용하지 마세요.
- 테스트 대상 Flask 앱은 로컬 전용입니다. GitHub Pages에서 실행되지 않습니다.
- Flask 앱과 자동화 실행을 함께 재현하려면 테스트 대상의 `templates/` 등 관련 파일, Python 의존성, 서버 실행이 추가로 필요합니다. 공개된 소스 4종은 자동화 로직 열람용입니다.
- 원본 Python 자동화는 `01_data` 폴더의 CSV를 읽습니다. 예시 프로젝트 구조:

```text
login-automation-local/
  01_data/
    login_validation.csv
    login_authentication.csv
  02_scripts/
    01_Test_login_validation.py
    02_Test_authentication.py
```

## 업로드
ZIP 압축을 해제한 **내용 전체**를 기존 GitHub 저장소 루트에 반영하세요. `index.html`과 `styles.css`, `projects.js` 등 기존 파일도 새 버전으로 교체해야 메인 페이지의 링크가 갱신됩니다. 기존 Pages 설정은 그대로 둡니다.

## 집계 출처
- 수동: 제출한 TC 엑셀 결과 43 PASS (사용자의 수동 실행 진술과 일치)
- 자동: 제공된 콘솔 캡처의 Validation 25 PASS / Authentication 9 PASS
- 자동화하지 않은 TC: 023, 024, 037–043 (9개)
- 자동화 코드는 제공된 파일 그대로 공개했고 변경하지 않았습니다. 일부 판정 조건 보강은 후속 개선으로 명시했습니다.
