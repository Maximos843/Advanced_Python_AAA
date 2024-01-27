import abc


class ComputerColor(abc.ABC):
    @abc.abstractmethod
    def __repr__(self):
        pass


class Color(ComputerColor):
    def __init__(self, red: int, green: int, blue: int):
        self._red = red
        self._green = green
        self._blue = blue

    def __repr__(self) -> str:
        END = '\033[0'
        START = '\033[1;38;2'
        MOD = 'm'
        return f'{START};{self._red};{self._green};{self._blue}{MOD}●{END}{MOD}'


if __name__ == '__main__':
    red = Color(0, 255, 0)
    print(red)
