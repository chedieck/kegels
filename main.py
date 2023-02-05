from time import sleep
from termcolor import colored
import os


class KegelState:
    HOLD = 1
    RELEASE = 2
    HOLDING = 3
    HELD = 4
    RELEASING = 5
    RELEASED = 6

    HOLD_TEXT = 'Hold'
    RELEASE_TEXT = 'Release'
    HOLDING_TEXT = 'Holding'
    HELD_TEXT = 'Held'
    RELEASING_TEXT = 'Releasing'
    RELEASED_TEXT = 'Released'

    HOLD_COLOR = 'red'
    RELEASE_COLOR = 'blue'
    HOLDING_COLOR = 'cyan'
    HELD_COLOR = 'red'
    RELEASING_COLOR = 'magenta'
    RELEASED_COLOR = 'blue'

    COLOR_MAP = {
        HOLD: HOLD_COLOR,
        RELEASE: RELEASE_COLOR,
        HOLDING: HOLDING_COLOR,
        HELD: HELD_COLOR,
        RELEASING: RELEASING_COLOR,
        RELEASED: RELEASED_COLOR,
    }

    TEXT_MAP = {
        HOLD: HOLD_TEXT,
        RELEASE: RELEASE_TEXT,
        HOLDING: HOLDING_TEXT,
        HELD: HELD_TEXT,
        RELEASING: RELEASING_TEXT,
        RELEASED: RELEASED_TEXT,
    }

    @classmethod
    def _get_number_of_before_and_after_text(cls, text):
        t_size = os.get_terminal_size()
        area = t_size.lines * t_size.columns
        text_len = len(text)
        empty_area = area - text_len
        if t_size.lines % 2:
            return (empty_area // 2, empty_area // 2)
        else:
            return (empty_area // 2 - t_size.columns // 2, empty_area // 2 + t_size.columns // 2)

    @classmethod
    def format_text(cls, kegel_state, elapsed_text):
        text = cls.TEXT_MAP[kegel_state] + elapsed_text
        left_padding, right_padding = cls._get_number_of_before_and_after_text(text)
        left_text_padding = colored(
            ' ' * left_padding,
            cls.COLOR_MAP[kegel_state],
            attrs=['reverse']
        )
        right_text_padding = colored(
            ' ' * right_padding,
            cls.COLOR_MAP[kegel_state],
            attrs=['reverse']
        )
        return (left_text_padding
                + text
                + right_text_padding)


def prompt():
    aux = input("Ready to start? [Y/n]")
    if not aux.upper() == 'N':
        for i in [3, 2, 1]:
            print(f"{i}...", end='\r')
            sleep(1)


def clear():
    t_size = os.get_terminal_size()
    area = t_size.lines * t_size.columns
    print(" " * area, end='\r')


def rest(segundos=20):
    clear()
    for i in range(segundos, 0, -1):
        print(f"Resting! ({i}s remaining)", end='\r')
        sleep(1)
    clear()


def yield_seconds(total=30):
    for i in range(total, 0, -1):
        yield f" ({i}s remaining)", i


def _run_set(total, step, i, state):
    for message, remaining_time in yield_seconds(total=step):
        elapsed_text = f"{message} (elapsed: {i*step + (step -remaining_time):^5}s/{total})"
        print(KegelState.format_text(state, elapsed_text), end='\r')
        sleep(1)

def single(state, total=120):
    _run_set(total=total, step=total, i=0, state=state)


def alternated(total=60, step=5):
    for i in range(total // step):
        if i % 2:
            state = KegelState.RELEASE
        else:
            state = KegelState.HOLD

        _run_set(total=total,
                 step=step,
                 i=i,
                 state=state
                 )


def full_circle(total=120, step=5):
    for i in range(total // step):
        if i % 4 == 0:
            state = KegelState.HOLDING
        elif i % 4 == 1:
            state = KegelState.HELD
        elif i % 4 == 2:
            state = KegelState.RELEASING
        elif i % 4 == 3:
            state = KegelState.RELEASED

        _run_set(total=total, step=step, i=i, state=state)


def first_routine():
    prompt()

    # first set
    hold_time = [1, 2, 3, 5, 10]
    for h in hold_time:
        alternated(60, h)

    clear()
    rest(20)

    # second set
    full_circle(total=120, step=5)
    rest(20)

    # third set
    alternated(60, 30)

    # fourth set
    single(KegelState.HOLD)

def second_routine():
    prompt()

    # first set
    hold_time = [10]
    for h in hold_time:
        alternated(120, h)

    clear()
    rest(15)

    # second set
    full_circle(total=160, step=8)
    rest(15)

    # third set
    alternated(120, 60)

    # fourth set
    single(KegelState.HOLD)



if __name__ == '__main__':
    # first_routine()
    second_routine()
    single(KegelState.HOLD)
    clear()
    print("Kegels done.")
