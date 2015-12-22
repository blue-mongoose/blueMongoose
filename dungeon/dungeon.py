from random import randint, choice, random
from time import sleep

limit = 20
tiles = 30
min = 20

directions = [lambda val: (val[0], val[1]+1),
              lambda val: (val[0], val[1]-1),
              lambda val: (val[0]+1, val[1]),
              lambda val: (val[0]-1, val[1])]

deadend = .2
hallway = .6
threeway = .1
fourway = .1

def gen_dungeon():
    dungeon = []

    for i in range(limit):
        tmp_list = []
        for j in range(limit):
            tmp_list.append(" ")
        dungeon.append(tmp_list)
    start = (10, 10)
    dungeon[start[0]][start[1]] = "@"
    undeveloped = []
    developed = []
    blocked = []
    deadends = []
    for i in range(0, randint(2, 4)):
        start_val = choice(directions)(start)
        undeveloped.append(start_val)
        dungeon[start_val[0]][start_val[1]] = "%"
        blocked.append(start_val)
    tile_count = 0
    while tile_count < tiles and len(undeveloped) > 0:
        # print_dungeon(dungeon)
        cur_tile = choice(undeveloped)
        passages = random()
        if passages < deadend:
            passage_num = 1
            deadends.append(cur_tile)
        elif passages < deadend + hallway:
            passage_num = 2
        elif passages < deadend + hallway + threeway:
            passage_num = 3
        else:
            passage_num = 4
        cur_undeveloped = []
        # print(passage_num)
        # print(cur_tile)
        # print("Developed: ", developed)
        # print("Undeveloped: ", undeveloped)
        # print("Blocked: ", blocked)
        for i in range(0, passage_num):
            for j in range(0, 5):
                tile_gen = choice(directions)(cur_tile)
                if tile_gen not in developed and tile_gen not in blocked and tile_gen not in cur_undeveloped:
                    break
            A = tile_gen[0] < limit and tile_gen[1] < limit
            B = tile_gen[0] > 0 and tile_gen[1] > 0
            if A and B and dungeon[tile_gen[0]][tile_gen[1]] == " " and tile_gen not in blocked:
                undeveloped.append(tile_gen)
                dungeon[tile_gen[0]][tile_gen[1]] = " "
                cur_undeveloped.append(tile_gen)
        for i in [x(cur_tile) for x in directions]:
            A = i not in cur_undeveloped
            B = i not in blocked
            C = i[0] < limit and i[1] < limit
            D = i[0] > 0 and i[1] > 0
            if A and B and C and D and dungeon[i[0]][i[1]] not in ["#", "@"]:
                blocked.append(i)
                dungeon[i[0]][i[1]] = " "
                try:
                    undeveloped.remove(i)
                except ValueError:
                    pass
        undeveloped.remove(cur_tile)
        dungeon[cur_tile[0]][cur_tile[1]] = "#"
        developed.append(cur_tile)
        tile_count += 1
        # sleep(1)

    # boss_tile = choice(deadends)
    # dungeon[boss_tile[0]][boss_tile[1]] = "!"

    # print(sorted(set(blocked)))
    if len(developed) >= min:
        # boss_tile = choice(developed)
        boss_tile = max([(distance(start, x), x) for x in developed])[1]
        developed.remove(boss_tile)
        stair_tile = max([(distance(start, x), x) for x in developed])[1]
        dungeon[boss_tile[0]][boss_tile[1]] = "!"
        dungeon[stair_tile[0]][stair_tile[1]] = "?"

        return dungeon
    else:
        return gen_dungeon()

def distance(pointA, pointB):
    return abs(pointA[0] - pointB[0]) + abs(pointA[1] - pointB[1])

def print_dungeon(dungeon):
    for i in dungeon:
        print(" ".join(map(str, i)))

for i in range(1, 100):
    print_dungeon(gen_dungeon())
