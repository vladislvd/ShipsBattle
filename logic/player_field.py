class PlayerField:
    def __init__(self):
        self.field = []
        with open('logic/player_field.txt', 'r') as file:
            for line in file:
                line = line.strip()
                row = []
                for char in line:
                    row.append(int(char))
                self.field.append(row)

    def get_field(self):
        return self.field

    def attack(self, x, y):
        pass
        # 0 - вода
        # 1 - корабль
        # 2 - мимо
        # 3 - попадание
