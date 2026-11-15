"""게임 전체를 관리하는 QuizGame 클래스."""

import random
from quiz import Quiz

LINE = "=" * 40
SUB_LINE = "-" * 40



def create_default_quizzes():
    """기본 퀴즈(주제: Python 기초)."""
    return [
        Quiz(
            "Python을 만든 사람은?",
            ["귀도 반 로섬", "리누스 토르발스", "제임스 고슬링", "데니스 리치"],
            1,
            "이름이 'G'로 시작합니다.",
        ),
        Quiz(
            "화면에 값을 출력할 때 사용하는 함수는?",
            ["input()", "print()", "len()", "open()"],
            2,
            "'인쇄하다'라는 뜻의 영어 단어입니다.",
        ),
        Quiz(
            "리스트의 길이(요소 개수)를 구하는 함수는?",
            ["size()", "count()", "len()", "length()"],
            3,
            "length의 줄임말입니다.",
        ),
        Quiz(
            "Python에서 한 줄 주석을 시작하는 기호는?",
            ["#", "//", "--", "/*"],
            1,
            "해시(샵) 기호입니다.",
        ),
        Quiz(
            "함수를 정의할 때 사용하는 키워드는?",
            ["function", "func", "define", "def"],
            4,
            "define의 줄임말입니다.",
        ),
        Quiz(
            "type(3.14)의 결과로 알맞은 자료형은?",
            ["int", "float", "str", "bool"],
            2,
            "소수점이 있는 숫자를 나타내는 자료형입니다.",
        ),
        Quiz(
            "다음 중 한 번 만들면 내용을 변경할 수 없는 자료형은?",
            ["list", "dict", "tuple", "set"],
            3,
            "소괄호 ( )로 만듭니다.",
        ),
    ]


class QuizGame:
    """퀴즈 목록과 점수를 가지고 게임 전체 흐름을 관리한다."""

    MENU_PLAY = 1
    MENU_ADD = 2
    MENU_LIST = 3
    MENU_SCORE = 4
    MENU_DELETE = 5
    MENU_EXIT = 6

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None  # 아직 퀴즈를 풀지 않았으면 None
        self.history = []       # 모든 게임 기록

    def input_number(self, prompt, minimum, maximum):
        """minimum~maximum 범위의 정수를 입력받을 때까지 반복한다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("[!] 입력이 비어 있습니다. 숫자를 입력하세요.")
                continue
            try:
                number = int(text)
            except ValueError:
                print(f"[!] 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
                continue
            if number < minimum or number > maximum:
                print(f"[!] 잘못된 입력입니다. {minimum}-{maximum} 사이의 숫자를 입력하세요.")
                continue
            return number

    def show_menu(self):
        print()
        print(LINE)
        print("        나만의 퀴즈 게임")
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print(LINE)

    def run(self):
        """메뉴를 반복해서 보여 주고, 선택한 기능을 실행한다."""
        while True:
            self.show_menu()
            choice = self.input_number("선택: ", self.MENU_PLAY, self.MENU_EXIT)
            if choice == self.MENU_PLAY:
                self.play_quiz()
            elif choice == self.MENU_ADD:
                self.add_quiz()
            elif choice == self.MENU_EXIT:
                print("\n프로그램을 종료합니다.")
                break
            else:
                print("\n아직 준비 중인 기능입니다.")
            
    def input_answer(self, quiz):
        """정답 번호를 입력받는다. 반환값: (고른 번호, 힌트 사용 여부)"""
        used_hint = False
        while True:
            if quiz.has_hint() and not used_hint:
                prompt = "정답 입력 (1-4, 힌트는 h): "
            else:
                prompt = "정답 입력 (1-4): "

            text = input(prompt).strip()
            if text == "":
                print("[!] 입력이 비어 있습니다. 1-4 사이의 숫자를 입력하세요.")
                continue
            if text.lower() == "h":
                if not quiz.has_hint():
                    print("[!] 이 문제에는 힌트가 없습니다.")
                elif used_hint:
                    print(f"[힌트] {quiz.hint}")
                else:
                    used_hint = True
                    print(f"[힌트] {quiz.hint} (힌트 사용: 이 문제 점수 절반)")
                continue
            try:
                number = int(text)
            except ValueError:
                print("[!] 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
                continue
            if number < 1 or number > Quiz.CHOICE_COUNT:
                print("[!] 잘못된 입력입니다. 1-4 사이의 숫자를 입력하세요.")
                continue
            return number, used_hint

    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("\n[!] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        print(f"\n등록된 퀴즈는 총 {total}개입니다.")
        count = self.input_number(f"몇 문제를 풀까요? (1-{total}): ", 1, total)

        # 문제 순서를 랜덤하게 섞어서 count개를 뽑는다.
        selected = random.sample(self.quizzes, count)

        print(f"\n퀴즈를 시작합니다! (총 {count}문제)")

        correct_count = 0
        points = 0.0  # 정답 1점, 힌트를 쓰고 맞히면 0.5점

        for number, quiz in enumerate(selected, start=1):
            print()
            print(SUB_LINE)
            quiz.display(number)
            user_answer, used_hint = self.input_answer(quiz)

            if quiz.is_correct(user_answer):
                correct_count += 1
                if used_hint:
                    points += 0.5
                else:
                    points += 1
                print("[O] 정답입니다!")
            else:
                correct_text = quiz.choices[quiz.answer - 1]
                print(f"[X] 오답입니다. 정답은 {quiz.answer}번 ({correct_text}) 입니다.")

        score = round(points / count * 100)
        self.show_result(count, correct_count, score)
        print(LINE)

    def show_result(self, count, correct_count, score):
        print()
        print(LINE)
        print(f"결과: {count}문제 중 {correct_count}문제 정답! ({score}점)")

        
    def input_text(self, prompt):
        """비어 있지 않은 문자열을 입력받을 때까지 반복한다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("[!] 입력이 비어 있습니다. 다시 입력하세요.")
                continue
            return text

    def add_quiz(self):
            elif choice == self.MENU_LIST:
                self.show_quiz_list()
        print("\n새로운 퀴즈를 추가합니다.\n")

        question = self.input_text("문제를 입력하세요: ")
        choices = []
        for number in range(1, Quiz.CHOICE_COUNT + 1):
            choices.append(self.input_text(f"선택지 {number}: "))
        answer = self.input_number("정답 번호 (1-4): ", 1, Quiz.CHOICE_COUNT)
        hint = input("힌트 (없으면 그냥 Enter): ").strip()

        self.quizzes.append(Quiz(question, choices, answer, hint))
        print("\n퀴즈가 추가되었습니다!")

    
    def show_quiz_list(self):
        if len(self.quizzes) == 0:
            print("\n[!] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print(SUB_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(SUB_LINE)