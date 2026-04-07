class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number=None):
        if number is not None:
            print(f"\n[문제 {number}]")
        print(f"{self.question}\n")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")
        print()

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"]
        )
