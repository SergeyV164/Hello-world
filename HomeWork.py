from random import randint
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Попытка выстрела за пределы игровой доски"

class BoardUsedExpention(BoardException):
    def __str__(self):
        return "В эту клетку уже стреляли"

class BoardWrongShipExceptoin(BoardException):
    pass
class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Coordinates({self.x}, {self.y})"

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def coordinates(self):
        ship_coordinates = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_coordinates.append(Coordinates(cur_x, cur_y))
        return ship_coordinates

    def shooten(self, shot):
        return shot in self.coordinates

class Battleground:
    def __init__(self, hid = False, size = 6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field =[["0"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        board = ""
        board += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            board += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            board = board.replace("■", "0")
        return board

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0<= d.y < self.size))

    def contour(self, ship, verb = False):
        shift = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for d in ship.coordinates:
            for dx, dy in shift:
                cur = Coordinates(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.coordinates:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipExceptoin()
        for d in ship.coordinates:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedExpention()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Уничтожен!")
                    return False
                else:
                    print("Ранен!")
                    return True

        self.field[d.x][d.y] = "T"
        print("Не попал!")
        return False

    def begin(self):
        self.busy = []

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class Computer(Player):
    def ask(self):
        d = Coordinates(randint(0,5), randint(0, 5))
        print(f"Ходит компьютер: {d.x + 1} {d.y + 1} ")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Ошибка! Необходимо ввести 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Ошибка! Введите числа! ")
                continue
            x, y = int(x), int(y)
            return Coordinates(x - 1, y - 1)

class Game:
    def __init__(self, size=6):
        self.size = size
        player = self.random_board()
        comp = self.random_board()
        comp.hid = True

        self.ai = Computer(comp, player)
        self.us = User(player, comp)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [1, 1, 1, 1, 2, 2, 3]
        board = Battleground(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                ship = Ship(Coordinates(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipExceptoin:
                    pass
        board.begin()
        return board

    def greet(self):
        print("----------------------")
        print("   Приветствуем ")
        print(" в игре морской бой")
        print("----------------------")
        print(" формат ввода: x y")
        print(" х - номер строки ")
        print(" y - номер столбца")

    def loop(self):
        num = 0
        while True:
            print("-" * 15)
            print("Доска игрока:")
            print(self.us.board)
            print("-" * 15)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 15)
            if num % 2 == 0:
                print("Ходит игрок!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 15)
                print("Игрок выиграл!!!")
                break

            if self.us.board.count == 7:
                print("-" * 15)
                print("Компьютер победил!!!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


j = Game()
j.start()

