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
            print(f"Победитель {battle_ground[a[0]][a[1]]}!")
            return True
    return False


battle_ground = [
    ["X", " ", " "],
    [" ", "X", " "],
    [" ", " ", "X"]
]
print(winner())