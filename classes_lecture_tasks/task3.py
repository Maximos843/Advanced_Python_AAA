class BasePokemon():
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category

    def __repr__(self):
        return f'{self.name}/{self.category}'


class Pokemon(BasePokemon):
    pass


if __name__ == '__main__':
    charmander = Pokemon(name='Charmander', category='Lizard')
    print(charmander)
