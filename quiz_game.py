"""게임 전체(메뉴, 퀴즈 풀기/추가/목록/삭제, 점수, 저장)를 관리하는 QuizGame 클래스."""

import json
import random
from datetime import datetime
from pathlib import Path

from quiz import Quiz

# 데이터 파일: 프로젝트 루트의 state.json
STATE_FILE = Path(__file__).resolve().parent / "state.json"

LINE = "=" * 40
SUB_LINE = "-" * 40


def create_default_quizzes():
    """파일이 없거나 손상되었을 때 사용하는 기본 퀴즈(주제: Python 기초)."""
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
        self.quizzes = []
        self.best_score = None  # 아직 퀴즈를 풀지 않았으면 None
        self.history = []       # 모든 게임 기록
        self.load_state()

    # ------------------------------------------------------------
    # 입력 처리
    # ------------------------------------------------------------
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

    def input_text(self, prompt):
        """비어 있지 않은 문자열을 입력받을 때까지 반복한다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("[!] 입력이 비어 있습니다. 다시 입력하세요.")
                continue
            return text

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

    # ------------------------------------------------------------
    # 메뉴
    # ------------------------------------------------------------
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
        try:
            while True:
                self.show_menu()
                choice = self.input_number("선택: ", self.MENU_PLAY, self.MENU_EXIT)

                if choice == self.MENU_PLAY:
                    self.play_quiz()
                elif choice == self.MENU_ADD:
                    self.add_quiz()
                elif choice == self.MENU_LIST:
                    self.show_quiz_list()
                elif choice == self.MENU_SCORE:
                    self.show_score()
                elif choice == self.MENU_DELETE:
                    self.delete_quiz()
                else:
                    self.save_state()
                    print("\n데이터를 저장했습니다. 프로그램을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C 또는 입력 스트림 종료: 저장 후 안전하게 종료
            print("\n\n[!] 입력이 중단되었습니다. 데이터를 저장하고 종료합니다.")
            self.save_state()

    # ------------------------------------------------------------
    # 퀴즈 풀기
    # ------------------------------------------------------------
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
        self.update_score(count, correct_count, score)

    def show_result(self, count, correct_count, score):
        print()
        print(LINE)
        print(f"결과: {count}문제 중 {correct_count}문제 정답! ({score}점)")

    def update_score(self, count, correct_count, score):
        """기록을 남기고, 최고 점수와 비교해 갱신한 뒤 파일에 저장한다."""
        self.history.append(
            {
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total": count,
                "correct": correct_count,
                "score": score,
            }
        )

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")
        else:
            print(f"현재 최고 점수: {self.best_score}점")
        print(LINE)

        self.save_state()

    # ------------------------------------------------------------
    # 퀴즈 추가 / 목록 / 삭제
    # ------------------------------------------------------------
    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.\n")

        question = self.input_text("문제를 입력하세요: ")
        choices = []
        for number in range(1, Quiz.CHOICE_COUNT + 1):
            choices.append(self.input_text(f"선택지 {number}: "))
        answer = self.input_number("정답 번호 (1-4): ", 1, Quiz.CHOICE_COUNT)
        hint = input("힌트 (없으면 그냥 Enter): ").strip()

        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save_state()
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

    def delete_quiz(self):
        if len(self.quizzes) == 0:
            print("\n[!] 삭제할 퀴즈가 없습니다.")
            return

        self.show_quiz_list()
        total = len(self.quizzes)
        number = self.input_number(f"삭제할 퀴즈 번호 (1-{total}, 취소는 0): ", 0, total)
        if number == 0:
            print("삭제를 취소했습니다.")
            return

        removed = self.quizzes.pop(number - 1)
        self.save_state()
        print(f"\n삭제했습니다: {removed.question}")

    # ------------------------------------------------------------
    # 점수 확인
    # ------------------------------------------------------------
    def show_score(self):
        if self.best_score is None:
            print("\n[!] 아직 퀴즈를 풀지 않았습니다. 퀴즈를 먼저 풀어 보세요.")
            return

        print(f"\n최고 점수: {self.best_score}점")

        if len(self.history) > 0:
            print(f"\n최근 게임 기록 (전체 {len(self.history)}회 중 최근 5회)")
            print(SUB_LINE)
            for record in self.history[-5:]:
                print(
                    f"{record['datetime']} | "
                    f"{record['total']}문제 중 {record['correct']}문제 정답 | "
                    f"{record['score']}점"
                )
            print(SUB_LINE)

    # ------------------------------------------------------------
    # 파일 저장 / 불러오기 (state.json)
    # ------------------------------------------------------------
    def save_state(self):
        """퀴즈, 최고 점수, 기록을 state.json에 UTF-8로 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"[!] 파일 저장에 실패했습니다: {error}")

    def load_state(self):
        """state.json을 불러온다. 없거나 손상되었으면 기본 퀴즈를 사용한다."""
        if not STATE_FILE.exists():
            print("저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.reset_to_default()
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            quizzes, best_score, history = self.parse_state(data)
        except (OSError, ValueError) as error:
            # json.JSONDecodeError, UnicodeDecodeError도 ValueError의 한 종류다.
            print(f"[!] 데이터 파일이 손상되었습니다. 기본 퀴즈로 복구합니다. ({error})")
            self.reset_to_default()
            self.save_state()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        self.history = history

        if self.best_score is None:
            score_text = "없음"
        else:
            score_text = f"{self.best_score}점"
        print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})")

    def parse_state(self, data):
        """불러온 데이터를 검사해서 (퀴즈 목록, 최고 점수, 기록)으로 돌려준다."""
        if not isinstance(data, dict):
            raise ValueError("최상위 데이터가 dict가 아닙니다.")

        raw_quizzes = data.get("quizzes")
        if not isinstance(raw_quizzes, list):
            raise ValueError("quizzes 형식이 잘못되었습니다.")
        quizzes = [Quiz.from_dict(item) for item in raw_quizzes]

        best_score = data.get("best_score")
        if best_score is not None and type(best_score) is not int:
            raise ValueError("best_score 형식이 잘못되었습니다.")

        history = []
        raw_history = data.get("history", [])
        if not isinstance(raw_history, list):
            raise ValueError("history 형식이 잘못되었습니다.")
        for record in raw_history:
            if not isinstance(record, dict):
                raise ValueError("history 형식이 잘못되었습니다.")
            for key in ("datetime", "total", "correct", "score"):
                if key not in record:
                    raise ValueError("history 형식이 잘못되었습니다.")
            history.append(record)

        return quizzes, best_score, history

    def reset_to_default(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.history = []