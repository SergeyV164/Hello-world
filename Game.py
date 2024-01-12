battle_ground = [[" "] * 3 for i in range(3)]
def show_battle_ground():
    print(f"  0 1 2")
    print(f"0 {battle_ground[0][0]} {battle_ground[0][1]} {battle_ground[0][2]}")
    print(f"1 {battle_ground[1][0]} {battle_ground[1][1]} {battle_ground[1][2]}")
    print(f"2 {battle_ground[2][0]} {battle_ground[2][1]} {battle_ground[2][2]}")
def move():
    while True:
        coordinates = input("Твой ход: ").split()
        if len(coordinates) != 2:
            print(" Необходимо ввести 2 значения!")
            continue
        x, y = coordinates
        if not (x.isdigit()) or not (y.isdigit()):
            print("Необходимо вводить числа!")
            continue
        x, y = int(x), int(y)
        if 0 <= x <= 2 and 0 <= y <= 2:
            if battle_ground[x][y] == " ":
                return x, y
            else:
                print("Невозможный ход, клетка занята!")
        else:
            print("Ход вне игрового поля!")
def winner():
    win_coordinates = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                       ((0, 0), (1, 0), (2, 0)),
                       ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)), ((0, 0), (1, 1), (2, 2)),
                       ((2, 0), (1, 1), (0, 2))]
    for coordinates in win_coordinates:
        a = coordinates[0]
        b = coordinates[1]
        c = coordinates[2]
        if battle_ground[a[0]][a[1]] == battle_ground[b[0]][b[1]] == battle_ground[c[0]][c[1]] != " ":
            show_battle_ground()
            print(f"Победитель {battle_ground[a[0]][a[1]]}!")
            return True
    return False
move_number = 0
while True:
    move_number += 1
    show_battle_ground()
    if move_number % 2 == 1:
        print("Ход: крестики")
    else:
        print("Ход: нолики")
    x, y = move()
    if move_number % 2 == 1:
        battle_ground[x][y] = "X"
    else:
        battle_ground[x][y] = "0"
    if winner():
        break
    if move_number == 9:
        print("Победителя нет")
        break





