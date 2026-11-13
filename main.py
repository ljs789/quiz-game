# 1️⃣ 클래스 정의 (맨 위)
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self):
        """문제와 선택지를 화면에 출력"""
        print(self.question)
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def is_correct(self, user_answer):
        """사용자 답이 정답인지 확인 (True/False 반환)"""
        return user_answer == self.answer


# 2️⃣ 메뉴 함수
def print_menu():
    print("\n===== 퀴즈 게임 =====")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("====================")
# 퀴즈 목록 만들기 (main 함수 위에)
def make_quizzes():
    """퀴즈 여러 개를 만들어 리스트로 반환"""
    quizzes = [
        Quiz("파이썬 창시자는?", ["귀도", "린우스", "제임스", "데니스"], 1),
        Quiz("1 + 1 = ?", ["1", "2", "3", "4"], 2),
        Quiz("파이썬 파일 확장자는?", [".java", ".py", ".txt", ".c"], 2),
    ]
    return quizzes

# 퀴즈 풀기 기능 (main 함수 위에)
def play_quiz(quizzes):
    """퀴즈를 하나씩 풀고 점수를 계산"""
    score = 0  # 점수 시작은 0점

    for quiz in quizzes:        # 퀴즈를 하나씩 꺼내서
        print()                 # 보기 좋게 한 줄 띄움
        quiz.show()             # 문제 + 선택지 출력

        answer = input("정답 번호: ").strip()

        if not answer.isdigit():          # 숫자가 아니면
            print("숫자를 입력해주세요! 이 문제는 오답 처리돼요.")
            continue                      # 다음 문제로

        if quiz.is_correct(int(answer)):  # 정답이면
            print("정답입니다! 🎉")
            score += 1                    # 점수 +1
        else:
            print(f"틀렸어요. 정답은 {quiz.answer}번이었어요.")

    print(f"\n===== 결과: {len(quizzes)}문제 중 {score}개 정답! =====")
# 4️⃣ main 함수
def main():
    quizzes = make_quizzes()   # 퀴즈 목록 준비!

    try:
        while True:
            print_menu()
            choice = input("원하는 기능의 번호를 입력하세요: ").strip()

            if choice == "1":
                play_quiz(quizzes)
            elif choice == "2":
                print("퀴즈 추가 (준비 중...)")
            elif choice == "3":
                print("퀴즈 목록 (준비 중...)")
            elif choice == "4":
                print("점수 확인 (준비 중...)")
            elif choice == "5":
                print("프로그램을 종료합니다. 안녕히 가세요!")
                break
            else:
                print("1~5 사이의 숫자를 입력해주세요!")

    except (KeyboardInterrupt, EOFError):
        print("\n\n프로그램을 안전하게 종료합니다. 안녕히 가세요!")


# 5️⃣ 프로그램 시작점 (맨 아래!)
if __name__ == "__main__":
    main()