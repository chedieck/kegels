from time import sleep
from termcolor import colored
import os


class KegelState:
    SEGURA = 1
    SOLTA = 2
    CONTRAINDO = 3
    CONTRAIDO = 4
    SOLTANDO = 5
    SOLTO = 6

    SEGURA_TEXT = 'Segura'
    SOLTA_TEXT = 'Solta'
    CONTRAINDO_TEXT = 'Contraindo'
    CONTRAIDO_TEXT = 'Contraído'
    SOLTANDO_TEXT = 'Soltando'
    SOLTO_TEXT = 'Solto'

    SEGURA_COLOR = 'red'
    SOLTA_COLOR = 'blue'
    CONTRAINDO_COLOR = 'cyan'
    CONTRAIDO_COLOR = 'red'
    SOLTANDO_COLOR = 'magenta'
    SOLTO_COLOR = 'blue'

    COLOR_MAP = {
        SEGURA: SEGURA_COLOR,
        SOLTA: SOLTA_COLOR,
        CONTRAINDO: CONTRAINDO_COLOR,
        CONTRAIDO: CONTRAIDO_COLOR,
        SOLTANDO: SOLTANDO_COLOR,
        SOLTO: SOLTO_COLOR,
    }

    TEXT_MAP = {
        SEGURA: SEGURA_TEXT,
        SOLTA: SOLTA_TEXT,
        CONTRAINDO: CONTRAINDO_TEXT,
        CONTRAIDO: CONTRAIDO_TEXT,
        SOLTANDO: SOLTANDO_TEXT,
        SOLTO: SOLTO_TEXT,
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
    aux = input("Preparado pra começar? [Y/n]")
    if not aux.upper() == 'N':
        for i in [3, 2, 1]:
            print(f"{i}...", end='\r')
            sleep(1)


def clear():
    t_size = os.get_terminal_size()
    area = t_size.lines * t_size.columns
    print(" " * area, end='\r')


def descanso(segundos=20):
    clear()
    for i in range(segundos, 0, -1):
        print(f"Denscansando! ({i}s faltando)", end='\r')
        sleep(1)
    clear()


def yield_seconds(state, total=30):
    for i in range(total, 0, -1):
        yield f" ({i}s faltando)", i


def _run_set(total=None, step=None, i=None, state=None):
    for message, remaining_time in yield_seconds(state=state,
                                                 total=step):
        elapsed_text = f"{message} (elapsed: {i*step + (step -remaining_time):^5}s/{total})"
        print(KegelState.format_text(state, elapsed_text), end='\r')
        sleep(1)

def single(state, total=120):
    _run_set(total=total, step=total, i=0, state=state)


def alternado(total=60, step=5):
    for i in range(total // step):
        if i % 2:
            state = KegelState.SOLTA
        else:
            state = KegelState.SEGURA

        _run_set(total=total,
                 step=step,
                 i=i,
                 state=state
                 )


def full_circle(total=120, step=5):
    for i in range(total // step):
        if i % 4 == 0:
            state = KegelState.CONTRAINDO
        elif i % 4 == 1:
            state = KegelState.CONTRAIDO
        elif i % 4 == 2:
            state = KegelState.SOLTANDO
        elif i % 4 == 3:
            state = KegelState.SOLTO

        _run_set(total=total, step=step, i=i, state=state)


def first_routine():
    prompt()

    # first set
    hold_time = [1, 2, 3, 5, 10]
    for h in hold_time:
        alternado(60, h)

    clear()
    descanso(20)

    # second set
    full_circle(total=120, step=5)
    descanso(20)

    # third set
    alternado(60, 30)

    # fourth set
    single(KegelState.SEGURA)

def second_routine():
    prompt()

    # first set
    hold_time = [10]
    for h in hold_time:
        alternado(120, h)

    clear()
    descanso(15)

    # second set
    full_circle(total=160, step=8)
    descanso(15)

    # third set
    alternado(120, 60)

    # fourth set
    single(KegelState.SEGURA)



if __name__ == '__main__':
    # first_routine()
    second_routine()
    single(KegelState.SEGURA)
    clear()
    print("Kegels done.")
