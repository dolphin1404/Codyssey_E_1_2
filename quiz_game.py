import json
import os
import random
from quiz import Quiz

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

DEFAULT_QUIZZES = [
    {
        "question": "Python의 창시자는 누구인가?",
        "choices": ["제임스 고슬링", "귀도 반 로섬", "리누스 토르발스", "데니스 리치"],
        "answer": 2
    },
    {
        "question": "Python에서 리스트의 마지막 요소에 접근하는 인덱스는?",
        "choices": ["0", "last", "-1", "end"],
        "answer": 3
    },
    {
        "question": "Python에서 사용되는 들여쓰기의 기본 권장 크기는?",
        "choices": ["2칸", "4칸", "8칸", "탭 1개"],
        "answer": 2
    },
    {
        "question": "다음 중 Python의 변경 불가능한(immutable) 자료형은?",
        "choices": ["list", "dict", "set", "tuple"],
        "answer": 4
    },
    {
        "question": "Python에서 여러 줄 문자열을 표현할 때 사용하는 기호는?",
        "choices": ["''' 또는 \"\"\"", "/* */", "<!-- -->", "{{ }}"],
        "answer": 1
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
            quiz_count = len(self.quizzes)
            score_text = f"{self.best_score}점" if self.best_score is not None else "없음"
            print(f"  저장된 데이터를 불러왔습니다. (퀴즈 {quiz_count}개, 최고점수 {score_text})")
        except (json.JSONDecodeError, KeyError, TypeError):
            print("  데이터 파일이 손상되어 기본 데이터로 초기화합니다.")
            self._load_defaults()

    def _load_defaults(self):
        self.quizzes = [Quiz.from_dict(q) for q in DEFAULT_QUIZZES]
        self.best_score = None

    def save_state(self):
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
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
        print("  4. 점수 확인")
        print("  5. 종료")
        print("========================================")

    def play_quiz(self):
        if not self.quizzes:
            print("\n  등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        quizzes = list(self.quizzes)
        random.shuffle(quizzes)
        total = len(quizzes)
        correct = 0

        print(f"\n  퀴즈를 시작합니다! (총 {total}문제)")
        print("----------------------------------------")

        answered = 0
        try:
            for i, quiz in enumerate(quizzes, 1):
                quiz.display(number=i)
                answer = get_valid_input("  정답 입력: ", 1, 4)
                answered += 1

                if quiz.check_answer(answer):
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

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("  새로운 최고 점수입니다!")
            self.save_state()

    def add_quiz(self):
        print("\n  새로운 퀴즈를 추가합니다.\n")

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

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n  퀴즈가 추가되었습니다!")

    def show_quiz_list(self):
        if not self.quizzes:
            print("\n  등록된 퀴즈가 없습니다.")
            return

        total = len(self.quizzes)
        print(f"\n  등록된 퀴즈 목록 (총 {total}개)")
        print("----------------------------------------")
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"  [{i}] {quiz.question}")
        print("----------------------------------------")

    def show_score(self):
        if self.best_score is None:
            print("\n  아직 퀴즈를 풀지 않았습니다.")
        else:
            print(f"\n  최고 점수: {self.best_score}점")

    def run(self):
        while True:
            self.show_menu()
            choice = get_valid_input("  선택: ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                self.save_state()
                print("\n  게임을 종료합니다. 안녕히 가세요!")
                break
