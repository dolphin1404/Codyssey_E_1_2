class Quiz:
    def __init__(self, question, choices, answer, hint=None):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, number=None):
        if number is not None:
            print(f"\n[문제 {number}]")
        print(f"{self.question}\n")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")
        if self.hint:
            print(f"\n  (힌트 보기: 0 입력 | 점수 절반 차감)")

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        data = {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }
        if self.hint:
            data["hint"] = self.hint
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data.get("hint", None)
        )
