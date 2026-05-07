# PLAN — Calculator Class 개발 계획

## 1. 개요

| 항목 | 내용 |
|------|------|
| 문서 버전 | v1.0 |
| 작성일 | 2026-05-07 |
| 참조 문서 | docs/PRD.md v1.0 |
| 구현 언어 | Python 3 |

---

## 2. 디렉토리 구조

```
calculator/
├── src/
│   └── calculator.py       # Calculator 클래스 구현
└── tests/
    └── test_calculator.py  # 단위 테스트
```

---

## 3. 클래스 설계

### 3.1 내부 상태

| 속성 | 타입 | 설명 |
|------|------|------|
| `_history` | `list[dict]` | 연산 이력 목록 (외부 직접 접근 불가) |

### 3.2 메서드 설계

#### 입력 유효성 검사 (내부 헬퍼)
```python
def _validate(self, *args) -> None
```
- 각 인자가 `int` 또는 `float`인지 확인
- 아니면 `TypeError` 발생
- 모든 public 메서드 진입 시 호출

#### 이력 기록 (내부 헬퍼)
```python
def _record(self, operation: str, operands: list, result) -> None
```
- `{"operation": ..., "operands": ..., "result": ...}` 형태로 `_history`에 추가

#### 사칙연산 메서드
```python
def add(self, a, b) -> int | float
def subtract(self, a, b) -> int | float
def multiply(self, a, b) -> int | float
def divide(self, a, b) -> float          # b == 0 → ZeroDivisionError
```
- 각 메서드는 `_validate` 호출 → 연산 → `_record` 호출 → 결과 반환 순서로 동작

#### 이력 관리 메서드
```python
def get_history(self) -> list   # _history 복사본 반환 (REQ-NF-002)
def clear_history(self) -> None # _history = []
def reset(self) -> None         # clear_history 호출 (REQ-006)
```

---

## 4. 예외 처리 설계

| 상황 | 예외 | 발생 위치 |
|------|------|-----------|
| 제수가 0 | `ZeroDivisionError` | `divide()` |
| 숫자 아닌 값 입력 | `TypeError` | `_validate()` |

---

## 5. 테스트 계획

### 5.1 정상 케이스

| 테스트 ID | 대상 | 입력 | 기대 결과 |
|-----------|------|------|-----------|
| TC-001 | `add` | `3, 5` | `8` |
| TC-002 | `add` | `1.5, 2.5` | `4.0` |
| TC-003 | `subtract` | `10, 3` | `7` |
| TC-004 | `subtract` | `0.5, 0.2` | `0.3` |
| TC-005 | `multiply` | `4, 3` | `12` |
| TC-006 | `multiply` | `2.0, 3.0` | `6.0` |
| TC-007 | `divide` | `10, 4` | `2.5` |
| TC-008 | `divide` | `7, 2` | `3.5` |

### 5.2 엣지 케이스

| 테스트 ID | 대상 | 입력 | 기대 결과 |
|-----------|------|------|-----------|
| TC-009 | `add` | `0, 0` | `0` |
| TC-010 | `multiply` | `0, 999` | `0` |
| TC-011 | `divide` | `0, 5` | `0.0` |
| TC-012 | `subtract` | `-3, -1` | `-2` |

### 5.3 예외 케이스

| 테스트 ID | 대상 | 입력 | 기대 예외 |
|-----------|------|------|-----------|
| TC-013 | `divide` | `5, 0` | `ZeroDivisionError` |
| TC-014 | `add` | `"a", 1` | `TypeError` |
| TC-015 | `multiply` | `None, 2` | `TypeError` |
| TC-016 | `divide` | `1, "b"` | `TypeError` |
| TC-021 | `subtract` | `"x", 3` | `TypeError` |

### 5.4 이력 관리

| 테스트 ID | 대상 | 시나리오 | 기대 결과 |
|-----------|------|----------|-----------|
| TC-017 | `get_history` | 연산 2회 후 조회 | 2개 항목 반환 |
| TC-018 | `get_history` | 반환 목록 수정 후 재조회 | 내부 이력 불변 |
| TC-019 | `clear_history` | 연산 후 이력 초기화 | 빈 목록 반환 |
| TC-020 | `reset` | 연산 후 전체 초기화 | 이력 빈 목록 |

---

## 6. 구현 순서

```
1단계  _validate, _record 헬퍼 구현
2단계  add, subtract, multiply 구현
3단계  divide 구현 (ZeroDivisionError 처리 포함)
4단계  get_history, clear_history, reset 구현
5단계  TC-001 ~ TC-020 테스트 코드 작성 및 실행
```

---

## 6. 요구사항 추적표

| 요구사항 ID | 구현 메서드 | 테스트 ID |
|-------------|-------------|-----------|
| REQ-001 | `add` | TC-001, TC-002, TC-009, TC-014 |
| REQ-002 | `subtract` | TC-003, TC-004, TC-012, TC-021 |
| REQ-003 | `multiply` | TC-005, TC-006, TC-010, TC-015 |
| REQ-004 | `divide` | TC-007, TC-008, TC-011, TC-013, TC-016 |
| REQ-005 | `get_history`, `clear_history` | TC-017, TC-018, TC-019 |
| REQ-006 | `reset` | TC-020 |
| REQ-NF-001 | `_validate` | TC-014, TC-015, TC-016, TC-021 |
| REQ-NF-002 | `get_history` (복사본 반환) | TC-018 |
| REQ-NF-003 | 클래스 전체 설계 | — |
