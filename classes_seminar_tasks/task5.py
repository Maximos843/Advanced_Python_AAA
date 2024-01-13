import abc


class ComputerColor(abc.ABC):
    @abc.abstractmethod
    def __repr__(self):
        pass

    @abc.abstractmethod
    def __mul__(self):
        pass

    @abc.abstractmethod
    def __rmul__(self):
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

    def __add__(self, other):
        if not isinstance(other, Color):
            raise ValueError
        new_red = self.checker(self._red + other._red)
        new_blue = self.checker(self._blue + other._blue)
        new_green = self.checker(self._green + other._green)
        return Color(new_red, new_green, new_blue)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        cl = -256 * (1 - other)
        F = (259 * (cl + 255)) / (255 * (259 - cl))
        new_blue = self.checker(F * (self._blue - 128) + 128)
        new_red = self.checker(F * (self._red - 128) + 128)
        new_green = self.checker(F * (self._green - 128) + 128)
        return Color(new_red, new_green, new_blue)

    def __hash__(self):
        return (2 ** self._red + 3 ** self._green + 5 ** self._blue) % (2 ** 32 - 1)
