"""게임 전체를 관리하는 QuizGame 클래스."""

LINE = "=" * 40
SUB_LINE = "-" * 40


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

            if choice == self.MENU_EXIT:
                print("\n프로그램을 종료합니다.")
                break
            else:
                print("\n아직 준비 중인 기능입니다.")