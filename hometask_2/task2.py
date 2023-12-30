import sys
import datetime
from typing import Callable


def timed_output(function: Callable) -> Callable:
    ORIGINAL_SYS_WRITE = sys.stdout.write

    def my_write(template: str) -> None:
        if not template.strip():
            return
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ORIGINAL_SYS_WRITE(f'[{date}]: {template}\n')

    def wrapper(*args, **kwargs):
        sys.stdout.write = my_write
        result = function(*args, **kwargs)
        sys.stdout.write = ORIGINAL_SYS_WRITE
        return result

    return wrapper


@timed_output
def print_greeting(name: str) -> str:
    print(f'Hello, {name}!')


if __name__ == "__main__":
    print_greeting("Nikita")
