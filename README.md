# Calculator

Python으로 구현한 사칙연산 계산기입니다. 단일 `Calculator` 클래스와 대화형 CLI 실행기로 구성되며, 에이전트 기반 워크플로우(consistency-verifier → ai-action → compliance-verifier ∥ test-verifier)를 통해 개발되었습니다.

---

## 프로젝트 구조

```
calculator/
├── CLAUDE.md                      # 에이전트 워크플로우 정의
├── README.md
├── run.py                         # 대화형 CLI 실행기
├── agents/                        # 에이전트 역할 정의
│   ├── consistency-verifier.md
│   ├── ai-action.md
│   ├── compliance-verifier.md
│   └── test-verifier.md
├── docs/                          # 설계 문서
│   ├── PRD.md                     # 요구사항 정의서
│   └── PLAN.md                    # 개발 계획 및 테스트 계획
├── src/
│   └── calculator.py              # Calculator 클래스
└── tests/
    └── test_calculator.py         # 단위 테스트 (22개)
```

---

## 시작하기

### 요구사항

- Python 3.10 이상
- pytest (테스트 실행 시)

```bash
pip install pytest
```

### CLI 실행

```bash
python run.py
```

---

## 사용법

프로그램 실행 시 사용 가능한 명령어가 자동으로 출력됩니다.

```
=== Calculator ===
  Commands:
    <a> + <b>   addition
    <a> - <b>   subtraction
    <a> * <b>   multiplication
    <a> / <b>   division
    history     show operation history
    reset       reset calculator (clears history)
    man         show this help
    quit        exit program
```

### 예시

```
> 3 + 5
  8
> 10 / 4
  2.5
> 2.5 * 4
  10
> history
  3 + 5 = 8
  10 / 4 = 2.5
  2.5 * 4 = 10
> reset
  history cleared
> 5 / 0
  error: division by zero
> quit
```

---

## Calculator 클래스 API

`src/calculator.py`의 `Calculator` 클래스를 직접 사용할 수 있습니다.

```python
from calculator import Calculator

calc = Calculator()

calc.add(3, 5)        # 8
calc.subtract(10, 3)  # 7
calc.multiply(4, 3)   # 12
calc.divide(10, 4)    # 2.5

calc.get_history()    # 연산 이력 반환 (복사본)
calc.clear_history()  # 이력 초기화
calc.reset()          # 전체 초기화
```

### 메서드

| 메서드 | 반환 타입 | 설명 |
|--------|-----------|------|
| `add(a, b)` | `int \| float` | 덧셈 |
| `subtract(a, b)` | `int \| float` | 뺄셈 |
| `multiply(a, b)` | `int \| float` | 곱셈 |
| `divide(a, b)` | `float` | 나눗셈 (b=0이면 ZeroDivisionError) |
| `get_history()` | `list` | 연산 이력 복사본 반환 |
| `clear_history()` | `None` | 이력 초기화 |
| `reset()` | `None` | 전체 초기화 |

### 예외

| 예외 | 발생 조건 |
|------|-----------|
| `ZeroDivisionError` | `divide()` 호출 시 제수가 0 |
| `TypeError` | 숫자(`int`, `float`)가 아닌 값 입력 |

### 이력 항목 구조

```python
{
    "operation": "add",   # 연산 종류
    "operands": [3, 5],   # 입력 값
    "result": 8           # 연산 결과
}
```

---

## 테스트 실행

```bash
python -m pytest tests/test_calculator.py -v
```

```
22 passed in 0.03s
```

| 구분 | 테스트 ID | 내용 |
|------|-----------|------|
| 정상 | TC-001 ~ TC-008 | 사칙연산 정수·실수·음수 |
| 엣지 | TC-009 ~ TC-012 | 0 입력, 음수 조합 |
| 예외 | TC-013 ~ TC-016, TC-021 | ZeroDivisionError, TypeError |
| 이력 | TC-017 ~ TC-020, TC-022 | 이력 기록·불변성·초기화 |

---

## 에이전트 워크플로우

이 프로젝트는 Claude Code 에이전트 기반 워크플로우로 개발되었습니다.

```
[문서 입력]
     │
     ▼
consistency-verifier   문서 간 정합성 검증
     │
     ▼ 통과
ai-action              구현 코드 + 테스트 코드 생성
     │
     ├──────────────────────┐
     ▼                      ▼
compliance-verifier    test-verifier     (병렬 실행)
     │                      │
     └──────────┬───────────┘
                ▼ 둘 다 승인
          [최종 산출물 확정]
```

| 에이전트 | 역할 |
|----------|------|
| `consistency-verifier` | PRD ↔ PLAN 문서 간 불일치·누락 탐지 |
| `ai-action` | 기능 구현 코드 및 단위 테스트 생성 |
| `compliance-verifier` | 구현 코드가 요구사항을 충족하는지 검증 |
| `test-verifier` | 테스트 코드의 품질·커버리지 검증 |
