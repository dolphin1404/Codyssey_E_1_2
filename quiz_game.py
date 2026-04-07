import json
import os
import random
from datetime import datetime
from quiz import Quiz

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

DEFAULT_QUIZZES = [
    {
        "question": "Python의 창시자는 누구인가?",
        "choices": ["제임스 고슬링", "귀도 반 로섬", "리누스 토르발스", "데니스 리치"],
        "answer": 2,
        "hint": "네덜란드 출신의 프로그래머입니다."
    },
    {
        "question": "Python에서 리스트의 마지막 요소에 접근하는 인덱스는?",
        "choices": ["0", "last", "-1", "end"],
        "answer": 3,
        "hint": "음수 인덱스를 사용합니다."
    },
    {
        "question": "Python에서 사용되는 들여쓰기의 기본 권장 크기는?",
        "choices": ["2칸", "4칸", "8칸", "탭 1개"],
        "answer": 2,
        "hint": "PEP 8 스타일 가이드를 참고하세요."
    },
    {
        "question": "다음 중 Python의 변경 불가능한(immutable) 자료형은?",
        "choices": ["list", "dict", "set", "tuple"],
        "answer": 4,
        "hint": "소괄호 ()로 생성하는 자료형입니다."
    },
    {
        "question": "Python에서 여러 줄 문자열을 표현할 때 사용하는 기호는?",
        "choices": ["''' 또는 \"\"\"", "/* */", "<!-- -->", "{{ }}"],
        "answer": 1,
        "hint": "따옴표를 세 개 연속으로 사용합니다."
    },
]


def get_valid_input(prompt, min_val, max_val):
    while True:
        try:
            text = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            raise

        if text == "":
            print("  잘못된 입력입니다. 값을 입력해 주세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print(f"  잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.")
            continue

        if number < min_val or number > max_val:
            print(f"  잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.")
            continue

        return number


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.history = []
        self.load_state()

    def load_state(self):
        if not os.path.exists(STATE_FILE):
            self._load_defaults()
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score", None)
            self.history = data.get("history", [])
            quiz_count = len(self.quizzes)
            score_text = f"{self.best_score}점" if self.best_score is not None else "없음"
            print(f"  저장된 데이터를 불러왔습니다. (퀴즈 {quiz_count}개, 최고점수 {score_text})")
        except (json.JSONDecodeError, KeyError, TypeError):
            print("  데이터 파일이 손상되어 기본 데이터로 초기화합니다.")
            self._load_defaults()

    def _load_defaults(self):
        self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
        self.best_score = None
        self.history = []

    def save_state(self):
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "history": self.history
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError:
            print("  데이터 저장에 실패했습니다.")

    def show_menu(self):
        print("\n========================================")
        print("        나만의 퀴즈 게임")
        print("========================================")
        print("  1. 퀴즈 풀기")
        print("  2. 퀴즈 추가")
        print("  3. 퀴즈 목록")
        print("  4. 퀴즈 삭제")
        print("  5. 점수 확인")
        print("  6. 점수 기록")
        print("  7. 종료")
        print("========================================")

    def play_quiz(self):
        if not self.quizzes:
            print("\n  등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        quizzes = list(self.quizzes)
        random.shuffle(quizzes)
        total = len(quizzes)

        print(f"\n  전체 퀴즈: {total}문제")
        print(f"  몇 문제를 풀겠습니까? (1-{total}, 전체: Enter)")

        try:
            text = input("  문제 수: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  퀴즈를 취소합니다.")
            return

        if text == "":
            count = total
        else:
            try:
                count = int(text)
            except ValueError:
                print(f"  잘못된 입력입니다. 전체 {total}문제를 출제합니다.")
                count = total

            if count < 1 or count > total:
                count = min(max(count, 1), total)
                print(f"  범위를 조정하여 {count}문제를 출제합니다.")

        quizzes = quizzes[:count]
        correct = 0
        hint_used = 0

        print(f"\n  퀴즈를 시작합니다! (총 {count}문제)")
        print("----------------------------------------")

        answered = 0
        try:
            for i, quiz in enumerate(quizzes, 1):
                quiz.display(number=i)
                used_hint = False

                while True:
                    if quiz.hint:
                        answer = get_valid_input("  정답 입력 (힌트: 0): ", 0, 4)
                    else:
                        answer = get_valid_input("  정답 입력: ", 1, 4)

                    if answer == 0 and quiz.hint:
                        print(f"\n  힌트: {quiz.hint}\n")
                        used_hint = True
                        continue
                    elif answer == 0:
                        print("  잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
                        continue
                    break

                answered += 1
                if used_hint:
                    hint_used += 1

                if quiz.check_answer(answer):
                    if used_hint:
                        print("  정답입니다! (힌트 사용 - 0.5점)")
                        correct += 0.5
                    else:
                        print("  정답입니다!")
                        correct += 1
                else:
                    print(f"  오답입니다. 정답은 {quiz.answer}번입니다.")

                print("----------------------------------------")
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  퀴즈를 중단합니다. ({answered}문제까지 진행)")
            if answered == 0:
                return

        if answered == 0:
            return

        score = int(correct / answered * 100)
        print(f"\n  결과: {answered}문제 중 {correct}문제 정답! ({score}점)")
        if hint_used > 0:
            print(f"  (힌트 사용: {hint_used}회)")

        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": answered,
            "correct": correct,
            "score": score,
            "hint_used": hint_used
        }
        self.history.append(record)

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("  새로운 최고 점수입니다!")

        self.save_state()

    def add_quiz(self):
        print("\n  새로운 퀴즈를 추가합니다.\n")

        try:
            question = input("  문제를 입력하세요: ").strip()
            if question == "":
                print("  문제가 비어 있어 추가를 취소합니다.")
                return

            choices = []
            for i in range(1, 5):
                choice = input(f"  선택지 {i}: ").strip()
                if choice == "":
                    print("  선택지가 비어 있어 추가를 취소합니다.")
                    return
                choices.append(choice)

            answer = get_valid_input("  정답 번호 (1-4): ", 1, 4)

            hint = input("  힌트 (없으면 Enter): ").strip()
            if hint == "":
                hint = None
        except (KeyboardInterrupt, EOFError):
            print("\n\n  퀴즈 추가를 취소합니다.")
            return

        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n  퀴즈가 추가되었습니다!")

    def delete_quiz(self):
        if not self.quizzes:
            print("\n  등록된 퀴즈가 없습니다.")
            return

        self.show_quiz_list()

        try:
            index = get_valid_input("\n  삭제할 퀴즈 번호: ", 1, len(self.quizzes))
        except (KeyboardInterrupt, EOFError):
            print("\n\n  삭제를 취소합니다.")
            return

        removed = self.quizzes.pop(index - 1)
        self.save_state()
        print(f"\n  [{index}] \"{removed.question}\" 퀴즈가 삭제되었습니다.")

    def show_quiz_list(self):
        if not self.quizzes:
            print("\n  등록된 퀴즈가 없습니다.")
            return

        total = len(self.quizzes)
        print(f"\n  등록된 퀴즈 목록 (총 {total}개)")
        print("----------------------------------------")
        for i, quiz in enumerate(self.quizzes, 1):
            hint_mark = " [힌트]" if quiz.hint else ""
            print(f"  [{i}] {quiz.question}{hint_mark}")
        print("----------------------------------------")

    def show_score(self):
        if self.best_score is None:
            print("\n  아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"\n  최고 점수: {self.best_score}점")

    def show_history(self):
        if not self.history:
            print("\n  아직 게임 기록이 없습니다.")
            return

        print(f"\n  게임 기록 (총 {len(self.history)}회)")
        print("----------------------------------------")
        for i, record in enumerate(self.history, 1):
            date = record["date"]
            total = record["total"]
            correct = record["correct"]
            score = record["score"]
            hint = record.get("hint_used", 0)
            hint_text = f" | 힌트 {hint}회" if hint > 0 else ""
            print(f"  [{i}] {date} | {total}문제 중 {correct}문제 정답 | {score}점{hint_text}")
        print("----------------------------------------")

    def run(self):
        while True:
            self.show_menu()
            choice = get_valid_input("  선택: ", 1, 7)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.delete_quiz()
            elif choice == 5:
                self.show_score()
            elif choice == 6:
                self.show_history()
            elif choice == 7:
                self.save_state()
                print("\n  게임을 종료합니다. 안녕히 가세요!")
                break
