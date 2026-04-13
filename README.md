# Python 퀴즈 게임

## 실행 방법

```bash
python main.py
```

- Python 3.10 이상 필요
- 외부 라이브러리 불필요 (표준 라이브러리만 사용)

## 기능 목록

| 번호 | 기능 | 설명 |
|------|------|------|
| 1 | 퀴즈 풀기 | 랜덤 출제, 문제 수 선택, 힌트 사용 가능, 결과 표시 |
| 2 | 퀴즈 추가 | 새로운 퀴즈(문제, 선택지 4개, 정답, 힌트)를 등록 |
| 3 | 퀴즈 목록 | 등록된 모든 퀴즈의 문제를 목록으로 확인 |
| 4 | 퀴즈 삭제 | 등록된 퀴즈를 선택하여 삭제 |
| 5 | 점수 확인 | 최고 점수 확인 |
| 6 | 점수 기록 | 전체 게임 기록(날짜, 점수, 힌트 사용) 확인 |
| 7 | 종료 | 데이터 저장 후 프로그램 종료 |

## 파일 구조

```
Codyssey_E_1_2/
├── main.py          # 프로그램 진입점
├── quiz.py          # Quiz 클래스 (개별 퀴즈 표현)
├── quiz_game.py     # QuizGame 클래스 (게임 전체 관리)
├── state.json       # 퀴즈 데이터 및 최고 점수 저장 파일 (실행 시 생성)
├── .gitignore       # Git 제외 파일 목록
└── README.md        # 프로젝트 설명
```

## 데이터 파일 설명

### state.json

- **경로**: 프로젝트 루트 디렉터리
- **역할**: 퀴즈 데이터와 최고 점수를 영속적으로 저장
- **인코딩**: UTF-8
- **스키마**:

```json
{
    "quizzes": [
        {
            "question": "문제 텍스트",
            "choices": ["선택지1", "선택지2", "선택지3", "선택지4"],
            "answer": 1,
            "hint": "힌트 텍스트 (선택)"
        }
    ],
    "best_score": null,
    "history": [
        {
            "date": "2026-04-07 15:30:00",
            "total": 5,
            "correct": 4,
            "score": 80,
            "hint_used": 1
        }
    ]
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `quizzes` | array | 퀴즈 객체 목록 |
| `quizzes[].question` | string | 퀴즈 문제 |
| `quizzes[].choices` | array(string) | 4개의 선택지 |
| `quizzes[].answer` | int (1~4) | 정답 번호 |
| `quizzes[].hint` | string 또는 없음 | 힌트 (선택) |
| `best_score` | int 또는 null | 최고 점수 (미플레이 시 null) |
| `history` | array | 게임 기록 목록 |
| `history[].date` | string | 플레이 일시 |
| `history[].total` | int | 푼 문제 수 |
| `history[].correct` | number | 정답 수 (힌트 사용 시 0.5) |
| `history[].score` | int | 점수 (100점 만점) |
| `history[].hint_used` | int | 힌트 사용 횟수 |
