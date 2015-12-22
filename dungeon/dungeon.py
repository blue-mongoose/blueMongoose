from random import randint, choice, random

limit = 20
tiles = 30
# dungeon = [[" "] * limit for i in range(limit)]
dungeon = []
for i in range(limit):
    tmp_list = []
    for j in range(limit):
        tmp_list.append(" ")
    dungeon.append(tmp_list)


directions = [lambda val: (val[0], val[1]+1),
              lambda val: (val[0], val[1]-1),
              lambda val: (val[0]+1, val[1]),
              lambda val: (val[0]-1, val[1])]

deadend = .13
hallway = .6
threeway = .2
fourway = .07

def gen_dungeon():
    # start = (randint(0, limit-1), randint(0, limit-1))
    start = (10, 10)
    dungeon[start[0]][start[1]] = "@"
    undeveloped = []
    for i in range(0, randint(2, 4)):
        undeveloped.append(choice(directions)(start))
    # undeveloped = [x(start) for x in directions]
    blocked = []
    tile_count = 0
    while tile_count < tiles: # and len(undeveloped) > 0:
        cur_tile = choice(undeveloped)
        tile_code = choice(['#', '#'])
        passages = random()
        if passages < deadend:
            passage_num = 1
        elif passages < deadend + hallway:
            passage_num = 2
        elif passages < deadend + hallway + threeway:
            passage_num = 3
        else:
            passage_num = 4
        for i in range(0, passage_num + 1):
            tile_gen = choice(directions)
            new_tile = tile_gen(cur_tile)
            A = new_tile[0] < limit and new_tile[1] < limit
            B = new_tile[0] > 0 and new_tile[1] > 0
            if A and B and dungeon[new_tile[0]][new_tile[1]] == " " and new_tile not in blocked:
                undeveloped.append(new_tile)
        for i in [x(cur_tile) for x in directions]:
            if i not in undeveloped:
                blocked.append(i)
                try:
                    undeveloped.remove(i)
                except ValueError:
                    pass
        undeveloped.remove(cur_tile)
        dungeon[cur_tile[0]][cur_tile[1]] = tile_code
        tile_count += 1


def print_dungeon(dungeon):
    for i in dungeon:
        print(" ".join(map(str, i)))

gen_dungeon()
print_dungeon(dungeon)
