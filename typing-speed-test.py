import curses
import time
import random
import string

GREEN_BLACK_PAIR = 1
RED_BLACK_PAIR = 2

BACKSPACE_KEY = "KEY_BACKSPACE"
BACKSPACE_CHAR = "\b"
DELETE_CHAR = "\x7f"
ESCAPE_CHAR = "\x1b"
WHITESPACE_CHAR = " "

AVG_WORD_LEN = 5

SEC_IN_MIN = 60

STATUS_COMPLETED = "completed"
STATUS_QUIT = "quit"

SUPPORTED_CHARS = set(
    string.ascii_letters + string.digits + string.punctuation + WHITESPACE_CHAR
)


def display_welcome_screen(screen):
    screen.clear()
    screen.addstr(0, 0, "Welcome to Typing Speed Test!")
    screen.addstr(2, 0, "Press any key to start...")
    screen.refresh()
    screen.getkey()


def get_random_phrase():
    phrases = [
        "The quick brown fox jumps over the lazy dog.",
        "London is the capital of Great Britain.",
        "The cat sat on the mat and looked at the rat.",
        "The Atlantic Ocean is between the Americas and Europe.",
        "A zebra has black and white stripes.",
    ]

    return random.choice(phrases)


def display_speed_test_screen(screen, target_text, current_text_list, wpm=0):
    screen.clear()

    screen.addstr(0, 0, f"Speed: {wpm} wpm")
    screen.addstr(2, 0, target_text)

    for i, char in enumerate(current_text_list):
        correct_char = target_text[i]
        color = curses.color_pair(GREEN_BLACK_PAIR)

        if correct_char != char:
            color = curses.color_pair(RED_BLACK_PAIR)

        screen.addstr(2, i, char, color)

    screen.refresh()


def calc_wpm(start_time, input_len):
    duration_in_sec = max(time.time() - start_time, 1)

    return round(input_len / AVG_WORD_LEN / (duration_in_sec / SEC_IN_MIN))


def run_speed_test(screen):
    target_text = get_random_phrase()
    current_text_list = []

    wpm = 0
    start_time = time.time()

    screen.nodelay(True)

    while True:
        wpm = calc_wpm(start_time, len(current_text_list))

        display_speed_test_screen(screen, target_text, current_text_list, wpm)

        current_text = "".join(current_text_list)
        if current_text == target_text:
            status = STATUS_COMPLETED
            break

        try:
            input_key = screen.getkey()
        except:
            continue

        if input_key == ESCAPE_CHAR:
            status = STATUS_QUIT
            break

        if input_key in (BACKSPACE_KEY, BACKSPACE_CHAR, DELETE_CHAR):
            if len(current_text_list) > 0:
                current_text_list.pop()
        elif len(current_text_list) < len(target_text) and input_key in SUPPORTED_CHARS:
            current_text_list.append(input_key)

    screen.nodelay(False)

    return status, wpm


def display_result_screen(screen, status, wpm):
    screen.clear()

    if status == STATUS_COMPLETED:
        screen.addstr(0, 0, f"Speed: {wpm} wpm")
        screen.addstr(
            2,
            0,
            "Congratulations! You completed the test",
            curses.color_pair(GREEN_BLACK_PAIR),
        )
    else:
        screen.addstr(0, 0, "Speed: N/A wpm")
        screen.addstr(
            2, 0, "You didn't finish the test", curses.color_pair(RED_BLACK_PAIR)
        )

    screen.addstr(4, 0, "Press any key to try again or Esc to exit...")


def main(screen):
    curses.init_pair(GREEN_BLACK_PAIR, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(RED_BLACK_PAIR, curses.COLOR_RED, curses.COLOR_BLACK)

    display_welcome_screen(screen)

    while True:
        status, wpm = run_speed_test(screen)

        display_result_screen(screen, status, wpm)

        input_key = screen.getkey()
        if input_key == ESCAPE_CHAR:
            break


curses.wrapper(main)
