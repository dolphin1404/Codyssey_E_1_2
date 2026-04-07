from quiz_game import QuizGame


def main():
    try:
        game = QuizGame()
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  프로그램을 안전하게 종료합니다.")
        try:
            game.save_state()
        except Exception:
            pass


if __name__ == "__main__":
    main()
