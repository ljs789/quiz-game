"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제, 선택지 4개, 정답 번호(1~4), 힌트를 가진 퀴즈 한 문제."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer  # 1~4 중 하나의 번호
        self.hint = hint

    def display(self, number):
        """문제와 선택지를 화면에 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True를 반환한다."""
        return user_answer == self.answer

    def has_hint(self):
        return self.hint != ""

    def to_dict(self):
        """JSON으로 저장할 수 있도록 dict로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """dict에서 Quiz 객체를 만든다. 형식이 잘못되면 ValueError를 발생시킨다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터가 dict가 아닙니다.")

        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")
        hint = data.get("hint", "")

        if not isinstance(question, str) or question.strip() == "":
            raise ValueError("문제 형식이 잘못되었습니다.")
        if not isinstance(choices, list) or len(choices) != cls.CHOICE_COUNT:
            raise ValueError("선택지 형식이 잘못되었습니다.")
        if not all(isinstance(choice, str) for choice in choices):
            raise ValueError("선택지 형식이 잘못되었습니다.")
        if type(answer) is not int or not 1 <= answer <= cls.CHOICE_COUNT:
            raise ValueError("정답 형식이 잘못되었습니다.")
        if not isinstance(hint, str):
            hint = ""

        return cls(question, choices, answer, hint)