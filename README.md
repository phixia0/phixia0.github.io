# TH / Quality Notebook — portfolio v6

완전히 새롭게 제작한 메인 레이아웃과 새 색상 체계(웜 페이퍼 / 잉크 / 애시드 라임 / 코발트)를 사용합니다. 별도 UI 프레임워크 없이 순수 HTML, CSS, JavaScript로 작성했습니다.

## 배포
이 ZIP의 **내부 파일과 폴더 전체**를 `phixia0.github.io` 저장소의 루트에 업로드해 주세요. `index.html`, `styles.css`, `projects.js`, `app.js`, `projects/`를 함께 반영해야 합니다. 기존 GitHub Pages `main / (root)` 설정은 유지합니다.

## 페이지
- `/` 새 홈페이지
- `/projects/login-qa/` 기존 요구사항 분석, 43 TC 탐색, 요구사항 추적표, PDF/원본 다운로드 유지 + 새 Jira 가상 결함 2건
- `/projects/login-automation/` 기존 34건 자동화, 코드, 실행화면, CSV/소스 다운로드 유지 + 최신 Jira 연결

## 결함 보고 기록
- QAD-1: TC-032 / 계정 잠금 상태 인증 허용 가상 시나리오
- QAD-2: TC-043 관련 / 로그아웃 후 페이지 접근 허용 가상 시나리오
- 실제 수행: 수동 43 PASS, 자동화 34 PASS (제공 기록 기준)
- 실제 발견 결함: 0 / 가상 결함: 2 / 재검증: Not Run
- Jira 화면 스크린샷은 **Jira 사용 실습**의 증거이지 실제 결함 증빙이 아닙니다.
- 첨부된 PDF와 DOCX는 사용자가 제공한 원본을 그대로 보존했습니다. 원본 문서의 사소한 서식 및 오탈자는 수정하지 않았습니다.

## 변경 시 주의
- `qa_practice.db`, `.local_secret` 등 로컬 상태/비밀키 파일은 포함하지 않습니다.
- 페이지의 HTML 경로 및 `projects/login-qa/data.js`, `explorer.js`, 자동화 CSV 등은 기존 기능을 유지합니다.
- 화면이 오래된 경우 GitHub Pages 배포 완료 후 Ctrl+Shift+R을 사용하세요.


## v7 업데이트
메인 「검증의 기록」을 직사각형 프로젝트 카드 그리드 대신 번호/가이드 라인/타이포그래피 중심의 세로형 케이스 인덱스로 변경했습니다. Jira 가상 결함 관리 2건은 별도 항목으로 표시되며 클릭 시 로그인 QA 상세 페이지의 결함 실습 영역으로 이동합니다. 원본 산출물과 자동화 상세 페이지는 유지합니다.
