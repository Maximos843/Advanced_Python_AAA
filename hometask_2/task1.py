import sys
import datetime


ORIGINAL_SYS_WRITE = sys.stdout.write


def my_write(template: str) -> None:
    if not template.strip():
        return
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ORIGINAL_SYS_WRITE(f'[{date}]: {template}\n')


def main():
    sys.stdout.write = my_write
    print(input())
    sys.stdout.write = ORIGINAL_SYS_WRITE


if __name__ == "__main__":
    main()
