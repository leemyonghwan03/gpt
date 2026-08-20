# Gpt노션 개발 에이전트 지침

이 저장소는 **Gpt노션(GptNotion)** 개발 저장소다. Gpt노션은 한국 사내 업무환경을 위한 **로컬 우선(local-first) 문서·지식·데이터베이스·AI 업무 플랫폼**이다. HWP 친화 문서작성, Notion형 블록/DB, RAG, Team Pages, Local SQLite, Local MCP, AI Operator를 하나의 제품으로 통합한다.

이 문서는 이 저장소에서 작업하는 모든 AI/코딩 에이전트의 최우선 프로젝트 지침이다. 기존 Luna Chat Coder는 작업 연속성과 fallback을 위한 도구이며, 프로젝트의 실제 아키텍처·기능·검증 기준은 이 문서가 정의한다.

채팅 기반 disposable/sandbox 환경에서 작업할 때는 필요 시 `.agents/skills/luna-chat-coder/SKILL.md`도 읽는다. 단, Luna를 이유로 프로젝트 구조나 기술스택을 임의 변경하지 않는다.

---

## 1. 절대 원칙

1. **기존 확정 기능을 임의로 삭제·축소·대체하지 않는다.** 기능 추가는 원칙적으로 누적(additive) 방식으로 한다.
2. **사용자 데이터 보존이 기능 추가보다 우선한다.** 부분 저장, 반쪽 객체, orphan 데이터를 남기지 않는다.
3. **오류를 숨겨 해결한 것으로 취급하지 않는다.** `try/catch`로 삼키거나 UI만 우회하지 말고 root cause를 수정한다.
4. **AI 모델을 신뢰하지 않는다. Gpt노션이 최종 권한자다.** 모델은 판단/제안을 하고 실제 실행은 검증·권한 계층을 통과한다.
5. **기존 공통 엔진을 우회하는 AI 전용 구현을 만들지 않는다.** UI, AI Operator, Automation은 동일한 도메인 명령/엔진을 재사용한다.
6. **사용자가 요청하지 않은 UI 위치·디자인·동작 변경을 하지 않는다.** 버그 수정은 최소 영향 범위로 한다.
7. **검증하지 않은 것을 PASS/완성이라고 보고하지 않는다.**

---

## 2. 제품 방향

Gpt노션은 단순 Notion clone이 아니다.

- **HWP식 문서작성 경험 + Notion식 구조화 데이터**
- **사내 폐쇄망/오프라인 우선**
- **IndexedDB / Local SQLite / Team JSON의 명확한 역할 분리**
- **사내 LLM, 로컬 LLM, OpenAI-compatible 모델을 수용하는 AI Operator**
- **RAG와 규정/매뉴얼 기반 업무문서 자동화**
- **Local MCP를 통한 SQLite, 파일파싱, Agent Job, Automation 확장**
- 한국 사무환경에서 실제 반복업무를 줄이는 것을 최우선으로 한다.

Notion에 기능이 있다는 이유만으로 복제하지 않는다. 실제 업무효과가 있는 기능을 우선한다.

---

## 3. 아키텍처 기준

### 3.1 Frontend

기본 배포 단위는 가능한 한 **단일 HTML**을 유지한다.

```text
개발 구조는 모듈화 가능
        ↓
빌드/배포 결과는 단일 HTML 우선
```

대규모 기능 추가 시 내부 모듈 분리는 허용하지만 사용자가 명시적으로 구조 변경을 요청하지 않았다면 기존 단일 HTML 사용성을 깨지 않는다.

### 3.2 저장소 역할

개인 데이터:

```text
기본        → IndexedDB
고급 로컬   → SQLite via Local MCP
```

팀 데이터:

```text
Team Pages → 사용자가 선택한 공유 폴더의 JSON 파일
```

규칙:

- Team용 SQLite 공유 DB를 임의로 만들지 않는다.
- 여러 사용자가 네트워크 드라이브의 하나의 SQLite 파일을 동시에 열도록 설계하지 않는다.
- Local SQLite 연결 실패 시 조용히 IndexedDB로 fallback하지 않는다. 데이터 분리를 막기 위해 명확히 오류를 표시한다.
- IndexedDB `DB_VERSION`은 명시적인 migration 작업이 아닌 이상 함부로 변경하지 않는다.

### 3.3 Local MCP

Local MCP는 단순 SQLite 서버가 아니라 Gpt노션의 로컬 백엔드/AI Gateway로 발전시킨다.

```text
Gpt노션 HTML
    ↓ localhost
GptNotion Local MCP
    ├ SQLite
    ├ Universal Model Gateway
    ├ Agent Jobs
    ├ FileSystem (허용 Root 기반)
    ├ PDF/HWP/HWPX/DOCX/XLSX/PPTX Parser
    ├ RAG/Embedding Worker
    ├ Backup/Restore
    ├ Encryption
    └ Background Automation
```

기존 Local DB 호환 포트/API를 깨지 않는다. 현재 호환 기준 포트는 `127.0.0.1:37841`이다.

Local MCP가 없어도 브라우저 기본 기능은 가능한 범위에서 정상 동작해야 한다. 단 사용자가 Local SQLite를 선택했다면 MCP 연결 실패를 명확히 알리고 저장 대상을 임의 변경하지 않는다.

---

## 4. 확정 기능 비회귀 목록

특별한 요청 없이 아래 기능을 제거·축소하지 않는다.

### Workspace / Page

- Sidebar / Topbar / Breadcrumb
- Page 생성, 선택, 제목, 아이콘, 부모/자식
- 즐겨찾기, 최근문서, 휴지통, 복구, 영구삭제
- Page duplicate
- 검색 / Inbox
- Import / Export
- Page Version / Share 구조
- @ Page Mention / Link / Backlink

### Editor

- Paragraph / H1 / H2 / H3 및 기존 Block type
- Enter / Shift+Enter / Tab / Shift+Tab / Backspace / Arrow key 동작
- Slash command (`/`)
- Mention (`@`)
- Block order/depth
- Document Board와 Block Editor 모드
- 한국어 IME 안정성
- HWP 친화 복사/붙여넣기

### Document Productivity

- 문서 조각(Snippet)
- `{{변수}}` 및 양식 자동완성
- Page Recipe
- 스마트 표
- 문서 ↔ DB 변환
- 규정 조항 자동 구조화
- AI 현재문서/선택영역 작업

### Database

- DB 생성/삭제
- Column/Row CRUD
- 기존 Property 타입
- Sort / Filter / Query
- Document/Table 연동

### RAG

- RAG Documents / Chunks / Embeddings
- 폴더 구조
- Retrieval V2
- BM25 계열 키워드 검색
- 한국어 synonym/가중치/rerank
- 인접 chunk 및 source line
- 기존 업로드 자료 재사용

### Team

- Team Pages ON/OFF / 공유 폴더 선택
- Page별 JSON 저장 / Team Page tree
- polling 동기화 / 충돌 감지
- 개인 → 팀 게시 / 팀 → 개인 사본
- 사용자 identity / 댓글/답글/resolve / Presence / Team Admin

기본 Team polling 값은 명시적 요구가 없는 한 유지한다. 현재 기준은 `POLL_MS = 5000`이다.

---

## 5. AI Operator 아키텍처

AI는 Gpt노션 기능을 직접 임의 함수 호출하지 않고 **Action/Tool 계층**을 통해 조작한다.

```text
사용자 요청
   ↓
Planner
   ↓
Tool Router / Model Gateway
   ↓
Entity Resolver
   ↓
Tool Contract
   ↓
Permission Policy
   ↓
Tool 실행
   ↓
Integrity Validator
   ↓
Verifier
   ↓
Audit / Diff / Provenance
```

필수 규칙:

- Tool 이름/인자는 스키마로 검증한다.
- 존재하지 않는 ID/잘못된 entity type을 실행 전에 막는다.
- `table.*`, `database.*`, `file.*`, `image.*` 전용 도메인은 범용 block update로 우회하지 않는다.
- Tool 실패를 자연어 성공으로 바꾸지 않는다.
- 동일 Tool+동일 인자 무한 반복을 차단한다.
- JSON parse 오류는 bounded repair를 수행하되 무한 retry하지 않는다.
- 큰 결과는 chunk/pagination을 사용한다.
- 장기 작업은 checkpoint/Agent Job으로 이어갈 수 있게 설계한다.

다음 Trust Core를 유지·강화한다.

- Tool Contract
- Entity Resolver
- Permission Policy
- Integrity Validator
- Transaction / Undo
- Diff
- Audit Log
- Source Provenance
- Planner / Verifier
- Operator Test Lab

모델이 바뀌어도 이 통제 계층은 Gpt노션이 소유한다.

---

## 6. Universal Model Gateway

Local MCP의 Model Gateway는 모델 차이를 흡수한다.

지원 방향:

- `/v1/chat/completions`
- `/v1/responses`
- 필요한 경우 legacy completions
- Ollama 계열 API
- vLLM / LM Studio / llama.cpp OpenAI-compatible endpoint 등

가능하면 모델별 system role 지원, JSON 준수도, Tool 선택 정확도, repair 빈도, context 한계, latency를 탐지/보정한다.

약한 모델에는 전체 Tool을 한꺼번에 노출하지 않는다. Router가 관련 Tool Pack만 좁혀 제공한다.

API Key, password, token 등의 secret은 로그/Audit/SQLite profile에 평문 저장하지 않는다.

---

## 7. 비동기 UI / 저장 안정성

단일 HTML에 비동기 저장, AI, Team sync가 많으므로 **UI lifecycle race를 항상 고려한다.**

금지 패턴:

```js
await something();
document.getElementById('x').textContent = value;
```

화면이 전환될 수 있는 비동기 작업 후에는 현재 View/Page/DOM 유효성을 검사한다.

필수 규칙:

- `await` 전에 대상 `pageId`, `blockId`, `databaseId`를 캡처한다.
- `await` 이후 `AppState.currentPageId`를 다시 읽어 대상 작업을 결정하지 않는다.
- Navigation epoch/token으로 stale completion을 무시한다.
- `renderPageHeader`, `renderEditor`, `renderBacklinks` 등은 DOM mount 여부를 방어한다.
- 데이터 commit과 UI refresh 오류를 분리한다.
- UI refresh 실패 때문에 저장 성공을 실패로 표시하지 않는다.
- Promise queue는 이전 rejected Promise 때문에 영구 poison되지 않도록 복구한다.
- 내부 flag(`rendering`, `undoBurst` 등)는 `finally`로 복원한다.
- async debounce rejection을 공통 error boundary에서 처리한다.
- overlay/modal event listener를 반복 누적하지 않는다.
- AI 응답 대기 중 selection/page가 바뀌면 stale selection을 실행하지 않는다.

`Cannot set properties of null`, stale DOM Range, 다른 페이지 오조작, 자동저장 queue 정지는 P0급 회귀로 취급한다.

---

## 8. Table / DB 데이터 무결성

### Table

행/열 추가·삭제·정렬 시 다음을 보존한다.

- merges
- rowspan / colspan
- 대표(master) 셀 내용
- colWidths
- rowHeights

병합 표를 조작할 때 전용 Table Engine을 사용한다. 병합정보를 `merges: []`로 초기화해서 문제를 숨기지 않는다.

### Database

- Database block의 `databaseId`는 실제 DB와 일치해야 한다.
- Column/Row는 존재하는 Database를 참조해야 한다.
- Page duplicate/copy 시 DB는 deep clone해야 한다.
- 범용 block type 변경으로 가짜 DB block을 만들지 않는다.
- 대량 분석은 모든 row를 모델 Context에 보내기보다 aggregate/group_by 계산 Tool을 우선한다.

---

## 9. Team Pages 안정성

Team Page는 일반 개인 Page와 편집 UX가 같지만 저장소는 다르다.

```text
Editor
 → serialize
 → conflict/signature check
 → Team JSON
```

- 파일명은 고정 Page ID 기반을 우선한다.
- 제목 변경으로 파일명을 바꾸지 않는다.
- 외부 변경을 감지하면 현재 편집 내용을 무조건 덮어쓰지 않는다.
- Undo는 AI 작업 이후 다른 팀원의 변경을 덮어쓰지 않도록 signature/CAS 검사를 수행한다.
- Presence/Comments/Config는 문서 JSON과 충돌 churn을 줄이기 위해 필요 시 별도 파일을 유지한다.
- Windows/사내 ACL이 실제 파일권한의 최종 경계다. 앱 role을 OS 권한처럼 과장하지 않는다.

---

## 10. 보안

- Secret/API Key/password/token을 저장소에 커밋하지 않는다.
- Audit log에 secret 원문을 남기지 않는다.
- Local MCP filesystem은 기본적으로 허용 root 밖을 접근하지 않는다.
- `../` path traversal을 차단한다.
- Team JSON 암호화는 Web Crypto 또는 검증된 표준 암호를 사용한다.
- 직접 만든 암호 알고리즘을 사용하지 않는다.
- AES-GCM 사용 시 IV reuse 금지.
- passphrase를 raw AES key로 직접 사용하지 않는다.
- 암호화 실패/잘못된 key에서 기존 파일을 빈 데이터로 overwrite하지 않는다.

---

## 11. 코딩 규칙

- 새 기능 전에 기존 구현을 검색한다.
- 동일 책임 함수/엔진을 중복 생성하지 않는다.
- 전역 이름 충돌과 정적 DOM ID 중복에 주의한다.
- 함수 이름은 역할을 드러내게 작성한다.
- 기존 상수/설정이 있으면 재사용한다.
- 기존 `DB_VERSION`, Team polling, endpoint normalization 값을 임의 변경하지 않는다.
- 사용자가 요구하지 않은 UI 재디자인을 하지 않는다.
- 한국어 UI 텍스트와 기존 용어를 가능한 한 유지한다.
- 대규모 단일 HTML 수정은 수정 전후 호출관계와 영향범위를 확인한다.

---

## 12. AI Endpoint 규칙

OpenAI-compatible endpoint 경로 중복을 만들지 않는다.

```text
Chat      → /v1/chat/completions
Responses → /v1/responses
```

Base URL만 입력하면 모드에 맞춰 경로를 붙이고, 이미 올바른 경로가 있으면 중복 부착하지 않는다.

연결 테스트, 모델 조회, 실제 요청은 공통 endpoint normalization 로직을 사용한다.

구형 서버가 system role을 거부하면 Gateway에서 호환 변환하되 system 지침 자체를 버리지 않는다.

---

## 13. 수정 후 필수 검증

### 정적 검사

- 전체 JavaScript syntax
- MCP 변경 시 Python `py_compile`
- 중복 정적 DOM ID
- Action/Tool 이름 중복
- `DB_VERSION` 의도치 않은 변경 여부
- Team `POLL_MS` 의도치 않은 변경 여부

### 핵심 smoke test

최소한 관련 변경 범위와 함께 다음 핵심 경로의 회귀를 확인한다.

1. 앱 초기화
2. 새 개인 Page 생성
3. Page 제목 변경
4. Document autosave
5. Page → 다른 View 빠른 전환
6. Page A → Page B 빠른 전환
7. Slash command
8. Mention / Backlink
9. Table 생성 및 행/열 수정
10. 병합 Table 경계조건
11. DB create/query/update
12. RAG search/read
13. IndexedDB 저장
14. Local MCP health
15. SQLite PUT/GET/DELETE
16. Team Page scan/save/conflict
17. AI Tool Contract validation
18. 위험 Tool Permission
19. Integrity check / rollback
20. AI 작업 전체 Undo

### 비동기 회귀 테스트

의도적으로 다음 race를 만든다.

- autosave 중 View 전환
- autosave 중 Page 전환
- AI 응답 대기 중 다른 Page 이동
- file picker 대기 중 다른 UI 조작
- Team sync 중 현재 Page 변경
- rejected save queue 이후 다음 저장

검증하지 못한 항목을 `PASS`라고 쓰지 않는다.

---

## 14. 버그 수정 절차

버그 보고를 받으면:

1. stack trace/재현 경로 확인
2. 정확한 실패 함수 확인
3. 해당 함수 호출자와 async boundary 확인
4. 데이터 오류인지 UI 오류인지 분리
5. root cause 수정
6. 같은 패턴을 전역 검색
7. 관련 회귀 테스트 추가
8. 기존 기능 보존 검사

예를 들어 `null.textContent` 오류가 나오면 해당 줄 하나에 `if(el)`만 추가하고 끝내지 않는다. 비동기 completion이 stale DOM을 만지는 구조가 있는지 전체 패턴을 검사한다.

---

## 15. Git / 저장소 작업

- 작업 전 현재 branch/commit SHA를 확인한다.
- 익숙하지 않은 파일/브랜치/사용자 변경을 임의 삭제하지 않는다.
- 다른 작업자의 변경을 덮어쓰지 않는다.
- 가능하면 기능별 branch에서 작업한다.
- 큰 변경은 하나의 목적 단위로 커밋한다.
- 사용자가 요청하지 않은 리팩터링을 같은 커밋에 섞지 않는다.
- 생성된 최종 artifact와 검증 source가 동일한지 확인한다.
- 저장소에 없는 파일/아키텍처를 대화 기억만으로 존재한다고 가정하지 않는다. GitHub의 durable source를 우선한다.

---

## 16. 완료 보고 기준

작업 완료 시 다음을 구분해 보고한다.

- 실제 변경한 파일
- 핵심 변경 내용
- 실행한 검사
- 각 검사 결과
- 실행하지 못한 검사와 이유
- 알려진 남은 위험/한계

`완성`, `정상`, `90점` 같은 표현은 실제 검증 근거가 있을 때만 사용한다.

---

## 17. 개발 우선순위

기능을 무작정 늘리기보다 다음 순서를 우선한다.

1. 기본 Page/Document/DB 저장 안정성
2. UI async/lifecycle 안정성
3. AI Tool 정확성 및 Trust Core
4. Universal Model Gateway
5. Local MCP + SQLite 통합
6. File Parser / RAG Worker
7. Persistent Agent Job / Background Automation
8. Team 보안/암호화
9. 유지보수 가능한 내부 모듈화 + 단일 HTML 배포

항상 **“기존 기능을 깨지 않고 실제 업무 성공률을 높이는가?”**를 최종 판단 기준으로 삼는다.
