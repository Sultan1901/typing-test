import curses
from curses import wrapper
import time
import random


def load_sentences(filepath="sentences.txt"):
    sentences = []
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line and ". " in line:
                    _, text = line.split(". ", 1)
                    sentences.append(text)
    except FileNotFoundError:
        sentences = ["The quick brown fox jumps over the lazy dog."]
    return sentences


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to the Speed Typing Test!", curses.color_pair(4))
    stdscr.addstr(2, 0, "A random sentence will be chosen for each round.")
    stdscr.addstr(3, 0, "Type it as fast and accurately as you can.")
    stdscr.addstr(5, 0, "Press any key to begin.", curses.color_pair(3))
    stdscr.refresh()
    stdscr.getkey()


def display(stdscr, target, current, wpm=0):
    stdscr.addstr(0, 0, target, curses.color_pair(4))
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        if i >= len(target):
            break
        color = curses.color_pair(1) if target[i] == char else curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def wpm_test(stdscr, target_text):
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            return wpm, True

        try:
            key = stdscr.getkey()
        except curses.error:
            continue

        if len(key) == 1 and ord(key) == 27:
            stdscr.nodelay(False)
            return wpm, False

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    sentences = load_sentences()
    start_screen(stdscr)

    while True:
        target_text = random.choice(sentences)
        wpm, completed = wpm_test(stdscr, target_text)

        stdscr.clear()
        if completed:
            stdscr.addstr(0, 0, f"Score: {wpm} WPM", curses.color_pair(3))
            stdscr.addstr(2, 0, "Congratulations! You completed the test.", curses.color_pair(1))
        else:
            stdscr.addstr(0, 0, "Test cancelled.", curses.color_pair(2))

        stdscr.addstr(4, 0, "Press any key to try again or 'Esc' to quit.")
        stdscr.refresh()

        key = stdscr.getkey()
        if len(key) == 1 and ord(key) == 27:
            break


wrapper(main)
