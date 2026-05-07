# Calculator Reviewer

## 전체 워크플로우

```
[문서 입력]
     │
     ▼
┌─────────────────────┐
│  consistency-       │  문서 간 정합성 검증
│  verifier           │  (PRD ↔ 설계 ↔ API 명세)
└─────────────────────┘
     │
     ├─ 불일치 발견 → 수정 요청 후 재검증
     │
     ▼ 통과
┌─────────────────────┐
│  ai-action          │  구현 코드 + 테스트 코드 생성
└─────────────────────┘
     │
     ▼
     ├────────────────────────┐
     │                        │
     ▼                        ▼
┌──────────────┐     ┌──────────────────┐
│  compliance- │     │  test-verifier   │  병렬 실행
│  verifier    │     │                  │
└──────────────┘     └──────────────────┘
     │                        │
     └───────────┬────────────┘
                 │
                 ├─ 어느 하나라도 반려 → ai-action 재실행
                 │
                 ▼ 둘 다 승인
            [최종 산출물 확정]
```

## 에이전트 역할 요약

| 에이전트 | 실행 시점 | 역할 |
|----------|-----------|------|
| `consistency-verifier` | 최초 단계 | 문서 간 용어·요구사항·API 명세 불일치 탐지 |
| `ai-action` | consistency-verifier 통과 후 | 기능 구현 코드 및 단위 테스트 코드 생성 |
| `compliance-verifier` | ai-action 완료 후 (병렬) | 구현 코드가 PRD·요구사항을 충족하는지 검증 |
| `test-verifier` | ai-action 완료 후 (병렬) | 테스트 코드의 품질·커버리지 검증 |

## 실행 규칙

- `consistency-verifier`가 불일치를 발견하면 `ai-action`은 실행되지 않는다.
- `compliance-verifier`와 `test-verifier`는 반드시 병렬로 실행된다.
- 두 verifier 중 하나라도 반려하면 `ai-action`부터 재실행한다.
- 최종 산출물은 두 verifier 모두 승인한 경우에만 확정된다.

## 에이전트 정의 위치

```
agents/
├── consistency-verifier.md
├── ai-action.md
├── compliance-verifier.md
└── test-verifier.md
```

## 참조 문서

| 문서 | 경로 | 설명 |
|------|------|------|
| PRD | `docs/PRD.md` | Calculator 클래스 기능·비기능 요구사항 정의 |
| PLAN | `docs/PLAN.md` | 클래스 설계, 테스트 계획, 요구사항 추적표 |
