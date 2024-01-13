class BasePokemon():
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category

    def to_str(self):
        print(f'{self.name}/{self.category}')


class Pokemon(BasePokemon):
    pass


if __name__ == '__main__':
    charmander = Pokemon(name='Charmander', category='Lizard')
    charmander.to_str()
