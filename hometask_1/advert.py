from keyword import iskeyword
import json


class Convert:
    """Class for initializing attributes from a json file"""
    def __init__(self, json_text: dict):
        if not isinstance(json_text, dict):
            raise TypeError
        for key, value in json_text.items():
            name = key
            if iskeyword(key):
                name = key + '_'
            if isinstance(value, list):
                setattr(
                    self,
                    name,
                    [Convert(elem) if isinstance(elem, dict) else elem for elem in value]
                )
            else:
                if isinstance(value, dict):
                    setattr(self, name, Convert(value))
                else:
                    setattr(self, name, value)


class ColorizeMixin:
    """Сlass Mixin for highlighting during output"""
    def __repr__(self, repr_color_code: int, template: str) -> str:
        return f'\033[0;{repr_color_code};40m {template} ₽'


class Advert(ColorizeMixin, Convert):
    """
    The final class with initialization of the keys and
    values of the json file, output and work with price.
    """
    repr_color_code = 32

    def __init__(self, json_text: dict):
        if 'title' not in json_text.keys():
            raise KeyError("Json data without title")
        try:
            if json_text['price'] < 0:
                raise ValueError("Price must be >= 0")
            json_text['price_'] = json_text.pop('price')
        except KeyError:
            json_text['price_'] = 0
        super().__init__(json_text)

    def __repr__(self) -> str:
        return super().__repr__(self.repr_color_code, f'{self.title} | {self.price}')

    @property
    def price(self) -> int:
        return self.price_

    @price.setter
    def price(self, value: int):
        if value < 0:
            raise ValueError("Price must be >= 0")
        self.price_ = value


if __name__ == '__main__':
    lesson_str = """{
    "title": "python",
    "price": 0,
    "location": {
    "address": "город Москва, Лесная, 7",
    "metro_stations": ["Белорусская"]
    }
    }"""
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    print(lesson_ad.location.address)
