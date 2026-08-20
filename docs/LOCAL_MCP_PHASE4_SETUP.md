# GptNotion Local MCP 4.0 — Universal Model Gateway

## 목적

Local MCP 하나를 실행하면 아래 기능이 동시에 동작합니다.

- 기존 GptNotion Local SQLite 저장소
- MCP `server/discover`, `tools/list`, `tools/call`
- Persistent Agent Jobs
- 제한된 Local Workspace
- Universal Model Gateway
- 모델 호환성 프로필 / 실제 사용 지표
- JSON 추출·복구
- 약한 모델용 Adaptive Tool Pack

기본 주소는 기존과 동일한 `http://127.0.0.1:37841`입니다. 기존 SQLite 데이터 경로도 그대로 사용합니다.

## Windows 실행

`start_gptnotion_local_mcp_v4.bat`

Python 3만 있으면 됩니다. 별도 pip 설치는 필요하지 않습니다.

기존 `gptnotion_local_engine.py` 또는 Local MCP 3.0이 같은 37841 포트에서 실행 중이면 먼저 종료합니다.

## AI 모델 연결

GptNotion의 기존 AI 설정에 다음을 입력합니다.

- Endpoint
- API Key (필요한 경우)
- Model

Phase 4 설정의 `모델 Adapter`는 기본 `자동 감지`를 권장합니다.

지원 Adapter:

1. OpenAI-compatible `/v1/chat/completions`
2. `/v1/responses`
3. Legacy `/v1/completions`
4. Ollama `/api/chat`

LM Studio, vLLM, llama.cpp 등 OpenAI-compatible 서버는 보통 Chat adapter로 동작합니다.

## 모델 적응 시험

설정 → `AI Operator 4차 · Universal Model MCP` → `모델 적응 테스트`

MCP가 Workspace를 수정하지 않는 짧은 테스트로 다음을 측정합니다.

- 연결 가능 여부
- JSON-only 준수
- Tool 선택 능력
- 인자 타입 준수
- 한 번에 Tool 하나 호출 규칙

점수에 따라 자동 전략을 선택합니다.

- 90~100: `fast` — 최대 36개 우선 Tool
- 75~89: `guided` — 최대 24개, Verifier 강화
- 55~74: `strict` — 최대 14개, Planner/Verifier 강제에 가깝게
- 0~54: `guarded` — 최대 8개, JSON 복구/한 Tool씩 실행 강화

실제 사용 중 JSON 복구·실패율도 SQLite `gateway_metrics`에 쌓이며, 충분한 표본이 생기면 실전 신뢰도를 프로필 점수에 반영합니다.

## 약한 모델 보강 기능

- 여러 `system` 메시지를 하나로 병합
- system role을 400/422로 거부하는 구형 서버는 첫 user 메시지의 `[SYSTEM INSTRUCTIONS]`로 자동 재시도
- 설명문/코드펜스가 섞인 JSON에서 JSON 객체 추출
- single quote 등 느슨한 Python식 dict도 안전 범위 내 정규화
- JSON 실패 시 모델에게 최대 1~3회 형식 복구 요청
- 존재하지 않는 Tool을 만들면 공개 Tool/system.find_tools로 재선택 요청
- 같은 Tool+같은 인자를 반복하면 `LOOP_GUARD`
- 실제 작업 요청인데 Tool 실행 전 `완료`라고 하면 `ACTION_REQUIRED`
- 모델 점수가 낮을수록 Tool schema 수를 자동 축소

## API Key 보안

API Key는 모델 호출 요청 때 Local MCP로 전달되지만 `model_profiles`, `gateway_metrics` SQLite 테이블에는 저장하지 않습니다.

Local MCP는 기본적으로 `127.0.0.1`에만 바인딩됩니다.

## 저장 위치

Windows 기본:

`%LOCALAPPDATA%\GptNotionLocal\`

- `data\gptnotion.db` — 개인 데이터 + Agent Jobs + Model Profiles/Metrics
- `backups\` — SQLite 백업
- `workspace\` — MCP 제한 파일 접근 폴더

## 현재 한계

“어떤 모델이든 동일한 품질”을 수학적으로 보장할 수는 없습니다. 아주 작은 모델이나 한국어/추론 능력이 부족한 모델은 MCP가 Tool 선택·JSON·반복실패를 크게 보완하더라도 결과 품질 자체에는 한계가 있습니다.

Phase 4의 목표는 모델별 차이를 최대한 MCP 내부에서 흡수하여 HTML/Tool 계층을 다시 수정하지 않게 만드는 것입니다.
