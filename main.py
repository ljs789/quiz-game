def print_menu():
    print("\n===== 퀴즈 게임 =====")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("====================")


def main():
    try:
        while True:
            print_menu()
            choice = input("원하는 기능의 번호를 입력하세요: ").strip()

            if choice == "1":
                print("퀴즈 풀기 (준비 중...)")
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
        # Ctrl+C 또는 입력 종료 시 여기로 점프
        print("\n\n프로그램을 안전하게 종료합니다. 안녕히 가세요!")


if __name__ == "__main__":
    main()