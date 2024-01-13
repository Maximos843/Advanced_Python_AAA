class EmojiMixin():
    def __repr__(self):
        emoj = {
            'grass': '🌿',
            'fire': '🔥',
            'water': '🌊',
            'electric': '⚡',
        }
        return f'{self.name}/{emoj[self.category]}'


class BasePokemon():
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category

    def __repr__(self):
        return f'{self.name}/{self.emoj[self.category]}'


class Pokemon(EmojiMixin, BasePokemon):
    pass


if __name__ == '__main__':
    pikachu = Pokemon(name='Pikachu', category='grass')
    print(pikachu)
