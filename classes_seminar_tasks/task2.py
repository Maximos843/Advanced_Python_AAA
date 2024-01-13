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

    def checker(self, value: int) -> int:
        return max(0, min(255, value))

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value: int):
        self._red = self.checker(value)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value: int):
        self._blue = self.checker(value)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value: int):
        self._green = self.checker(value)

    def __eq__(self, other):
        if not isinstance(other, Color):
            raise ValueError
        return (self._red == other._red) and \
            (self._blue == other._blue) and (self._green == other._green)


if __name__ == '__main__':
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    print(red == green)
    print(red == Color(255, 0, 0))
