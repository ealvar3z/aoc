import re

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))

def move(grid, d, i, j):
    ni, nj = i, j

    while True:
        ni, nj = add((ni, nj), DIRS[d])
        ni %= 200
        nj %= 150
        if (ni, nj) in grid:
            break

    if grid[ni, nj] == "#":
        return i, j

    return ni, nj


def _move(grid, d, i, j):
    nd, ni, nj = d, *add((i, j), DIRS[d])

    match nd, ni, nj:
        case 0, _, 150 if ni in range(50):
            nd, ni, nj = 2, 149-ni, 99
        case 0, _, 100 if ni in range(50, 100):
            nd, ni, nj = 3, 49, 50+ni
        case 0, _, 100 if ni in range(100, 150):
            nd, ni, nj = 2, 149-ni, 149
        case 0, _, 50 if ni in range(150, 200):
            nd, ni, nj = 3, 149, ni-100
        
        case 1, 200, _ if nj in range(50):
            nd, ni, nj = 1, 0, nj+100
        case 1, 150, _ if nj in range(50, 100):
            nd, ni, nj = 2, nj+100, 49
        case 1, 50, _ if nj in range(100, 150):
            nd, ni, nj = 2, nj-50, 99

        case 2, _, 49 if ni in range(0, 50):
            nd, ni, nj = 0, 149-ni, 0
        case 2, _, 49 if ni in range(50, 100):
            nd, ni, nj = 1, 100, ni-50
        case 2, _, -1 if ni in range(100, 150):
            nd, ni, nj = 0, 149-ni, 50
        case 2, _, -1 if ni in range(150, 200):
            nd, ni, nj = 1, 0, ni-100
        
        case 3, 99, _ if nj in range(50):
            nd, ni, nj = 0, 50+nj, 50
        case 3, -1, _ if nj in range(50, 100):
            nd, ni, nj = 0, nj+100, 0
        case 3, -1, _ if nj in range(100, 150):
            nd, ni, nj = 3, 199, nj-100

    if grid[ni, nj] == ".":
        return nd, ni, nj
    elif grid[ni, nj] == "#":
        return d, i, j


def part_one(f):
    grid, inst = f.read().split("\n\n")
    grid = grid.splitlines()
    grid = {(i, j): cell for i, row in enumerate(grid) for j, cell in enumerate(row) if cell != " "}

    inst = re.split(r"(?<=\d)(?=[LR])|(?<=[LR])(?=\d)", inst)
    d, i, j = 0, 0, next(j for j in range(150) if (0, j) in grid)

    for c in inst:
        match c:
            case "L":
                d -= 1
                d %= 4
            case "R":
                d += 1
                d %= 4
            case _:
                for _ in range(int(c)):
                    i, j = move(grid, d, i, j)

    return (i+1) * 1000 + (j+1) * 4 + d


def part_two(f):
    grid, inst = f.read().split("\n\n")
    grid = grid.splitlines()
    grid = {(i, j): cell for i, row in enumerate(grid) for j, cell in enumerate(row) if cell != " "}

    inst = re.split(r"(?<=\d)(?=[LR])|(?<=[LR])(?=\d)", inst)
    d, i, j = 0, 0, next(j for j in range(150) if (0, j) in grid)

    for c in inst:
        match c:
            case "L":
                d -= 1
                d %= 4
            case "R":
                d += 1
                d %= 4
            case _:
                for _ in range(int(c)):
                    d, i, j = _move(grid, d, i, j)

    return (i+1) * 1000 + (j+1) * 4 + d

