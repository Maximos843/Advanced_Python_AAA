import sys
from typing import Callable


def redirect_output(filepath: str) -> Callable:
    def wrapper(function: Callable) -> Callable:
        def decorator(*args, **kwargs) -> None:
            original_sys = sys.stdout
            with open(filepath, 'w+') as file:
                sys.stdout = file
                result = function(*args, **kwargs)
            sys.stdout = original_sys
            return result
        return decorator
    return wrapper


@redirect_output('./function_output.txt')
def calculate():
    for power in range(1, 5):
        for num in range(1, 20):
            print(num ** power, end=' ')
        print()


if __name__ == '__main__':
    calculate()
