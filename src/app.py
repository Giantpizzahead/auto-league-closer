import leaguecloser
import time


def main():
    print("Searching for League...")
    while True:
        if leaguecloser.is_league_running():
            print("\nNO LEAGUE ALLOWED!")
            if leaguecloser.close_league():
                print("\nThat's right... now get back to work!")
        time.sleep(3)


if __name__ == "__main__":
    main()
