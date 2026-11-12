// 새 프로젝트를 추가할 때 이 배열에 항목을 복사해서 수정하세요.
// category: manual / automation / defect / learning
// status: 진행 중 / 완료 / 예정
// link: 게시할 상세 페이지나 GitHub 주소. 아직 없다면 ""로 둡니다.
window.PORTFOLIO_PROJECTS = [
  {
    number: '01',
    category: 'manual',
    title: '로그인 기능 QA',
    english: 'LOGIN FEATURE TESTING',
    artwork: 'LOGIN<br>QA TEST',
    description: '10개 요구사항을 분석하고 12개 추가 확인사항을 정리했습니다. 43개 테스트 케이스를 수동 실행해 모두 PASS로 기록했습니다. 자동화한 34건과 수동 유지 9건의 구분, Jira 가상 결함 2건, 실제 산출물을 함께 확인할 수 있습니다.',
    tags: ['REQ 10개', '수동 43 PASS', '산출물 공개'],
    status: '기록 공개',
    link: 'projects/login-qa/index.html'
  },
  {
    number: '02',
    category: 'automation',
    title: '로그인 테스트 자동화',
    english: 'SELENIUM AUTOMATION',
    artwork: 'PYTHON<br>+ SELENIUM',
    description: 'CSV 기반 검증 25건과 로그인 인증 9건을 자동화했습니다. 실제 실행 기록, 주요 코드, CSV 데이터와 9건의 수동 유지 근거를 확인할 수 있습니다.',
    tags: ['34 PASS 기록', 'Selenium', 'CSV'],
    status: '기록 공개',
    link: 'projects/login-automation/index.html'
  },
  {
    number: '03',
    category: 'defect',
    title: 'Jira 결함 관리 실습',
    english: 'DEFECT TRACKING / JIRA',
    artwork: 'BUG<br>TRACKING',
    description: '실제 발견 결함은 0건입니다. 인증·세션 관련 가상 결함 QAD-1·QAD-2를 별도로 정의하고 Jira 등록, 가상 검토, 재검증 계획과 Word·PDF 보고서로 정리했습니다.',
    tags: ['가상 결함 2건', 'Ready for Retest', '보고서·Jira 증빙'],
    status: '가상 실습 공개',
    link: 'projects/login-qa/index.html#defect-simulation'
  },
  {
    number: '04',
    category: 'learning',
    title: '소프트웨어 테스트 학습 기록',
    english: 'TESTING STUDY NOTES',
    artwork: 'TESTING<br>NOTES',
    description: 'CSTS 학습 과정에서 익힌 테스트 설계 기법과 프로세스를 정리하고, 실제 실습에 적용한 내용을 차근차근 기록할 예정입니다.',
    tags: ['CSTS', '테스트 기법', '학습 기록'],
    status: '예정',
    link: ''
  }
];

// GitHub 사용자명 등록 후 아래 문자열을 바꿔 주세요. 예: 'my-github-id'
window.GITHUB_USERNAME = 'phixia0';
