# TH QA LAB — QA 포트폴리오 사이트

HTML, CSS, JavaScript로 만든 정적 포트폴리오입니다. 별도 서버나 유료 호스팅이 필요하지 않습니다.

## 미리 보기

`index.html`을 더블 클릭해 웹 브라우저로 열면 됩니다. (구글 폰트는 인터넷 연결 시 적용됩니다.)

## GitHub Pages에 올리는 방법 (브라우저만 이용)

1. GitHub에 로그인합니다.
2. 오른쪽 상단 `+` → `New repository`를 선택합니다.
3. Repository name에 `<본인GitHub아이디>.github.io`를 입력합니다. 예: `sampleuser.github.io`.
4. `Public`을 선택하고 `Create repository`를 누릅니다.
5. 새 저장소에서 `Add file` → `Upload files`를 클릭합니다.
6. **압축파일 자체를 올리지 말고**, 압축을 풀어 나온 `index.html`, `styles.css`, `app.js`, `projects.js`, `README.md` 파일을 전부 선택해 업로드합니다. 파일은 저장소 **최상위(root)** 에 있어야 합니다.
7. `Commit changes`를 누릅니다.
8. `Settings` → 왼쪽 `Pages` → `Build and deployment` → `Source: Deploy from a branch` → `Branch: main` / `/(root)` → `Save`를 선택합니다.
9. 몇 분 뒤 `https://<본인GitHub아이디>.github.io/`로 접속합니다. GitHub 공식 문서에 따르면 게시에 최대 약 10분 걸릴 수 있습니다.

### 이미 `<본인아이디>.github.io` 저장소가 있나요?

새로 만들지 말고 해당 저장소의 기존 파일과 충돌하지 않게 백업한 뒤 업데이트하세요.

## 수정할 곳

- `index.html`: 자기소개와 문구
- `styles.css`: 색상과 디자인
- `projects.js`: 프로젝트 카드 내용, 상태, 링크, GitHub 아이디
- `app.js`: 프로젝트 필터 등의 기능

`projects.js` 맨 아래 `window.GITHUB_USERNAME = '';`의 빈칸에 본인의 GitHub 사용자명을 입력하세요.

프로젝트 상세 페이지나 GitHub 주소가 준비되면 해당 프로젝트의 `link: ''`에 주소를 넣으세요. 링크가 비어 있으면 '기록 준비 중'으로 표시됩니다.

## 주의

- 진행 중/예정 상태의 항목은 완료한 성과로 표현하지 않았습니다. 실제 완성된 항목부터 갱신하세요.
- 개인 연락처, 실습용 비밀번호, 비공개 자료, 실제 서비스 계정정보는 공개 저장소에 올리지 마세요.
- 더 복잡한 프로젝트로 확장하더라도 지금의 파일 구조를 유지하면서 시작할 수 있습니다.
