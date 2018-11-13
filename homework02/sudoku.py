""" Sudoku solving and generating"""
import random


def read_sudoku(filename: str) -> list:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values: list) -> None:
    """Вывод Судоку"""
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: list, n: int) -> list:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    grouplist = []
    templist = []
    for i in range(0, len(values)//n * n, n):
        templist.clear()
        templist = [j for j in values[(0 + i): (n + i)]]
        grouplist.append(templist[:])
    return grouplist


def get_row(values: list, pos: tuple) -> list:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, col = pos
    return values[row]


def get_col(values: list, pos: tuple) -> list:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    ri, ci = pos
    return [row[ci] for row in values]


def get_block(values: list, pos: tuple) -> list:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    return [values[i][j] for i in range(row-row % 3, row-row % 3+3) for j in range(col-col % 3, col-col % 3+3)]


def find_empty_positions(grid: list) -> tuple:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if grid[i][j] == ".":
                return(i, j)
    return(-1, -1)


def find_possible_values(grid: list, pos: tuple) -> list:
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    return set('123456789') - set(get_row(grid, pos) + get_col(grid, pos) + get_block(grid, pos))


def solve(grid: list) -> list:
    """ Решение пазла, заданного в grid
        Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    row, col = pos
    if row < 0:
        return grid
    for pval in find_possible_values(grid, pos):
        grid[row][col] = pval
        newgrid = solve(grid)
        if newgrid:
            return newgrid
    grid[row][col] = '.'
    return None


def check_solution(solution: list) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False
    >>> grid = solve(read_sudoku('puzzle1.txt'))
    >>> display(grid)
    5 3 4 |6 7 8 |9 1 2
    6 7 2 |1 9 5 |3 4 8
    1 9 8 |3 4 2 |5 6 7
    ------+------+------
    8 5 9 |7 6 1 |4 2 3
    4 2 6 |8 5 3 |7 9 1
    7 1 3 |9 2 4 |8 5 6
    ------+------+------
    9 6 1 |5 3 7 |2 8 4
    2 8 7 |4 1 9 |6 3 5
    3 4 5 |2 8 6 |1 7 9

    >>> check_solution(grid)
    True
    >>> grid = read_sudoku('puzzle4.txt')
    >>> display(grid)
    8 3 5 |4 1 6 |9 2 7
    2 9 6 |8 5 7 |4 3 1
    4 1 7 |2 9 3 |6 5 8
    ------+------+------
    5 6 9 |1 3 4 |7 8 2
    1 2 3 |6 7 8 |5 4 9
    7 4 8 |5 2 9 |1 6 3
    ------+------+------
    6 5 2 |7 8 1 |3 9 4
    9 8 1 |3 4 5 |2 7 6
    3 7 4 |9 6 2 |8 1 8

    >>> check_solution(grid)
    False
    """
    order = frozenset('123456789')
    for i in range(0, len(solution)):
        setval = set(get_row(solution, (i, 0)))
        if setval != order:
            return False
    for i in range(0, len(solution)):
        setval = set(get_col(solution, (0, i)))
        if setval != order:
            return False
    for i in range(0, 8, 3):
        for j in range(0, 8, 3):
            setval = set(get_block(solution, (i, j)))
            if setval != order:
                return False
    return True


def generate_sudoku(N: int) -> list:
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = []
    temp = []
    for i in range(0, 9):
        temp.append(".")
    for i in range(0, 9):
        grid.append(temp[:])
    for i in range(0, 8, 3):
        grid[i][i] = str(random.randint(1, 9))
    grid = solve(grid)
    if N < 0:
        N = 0
    elif N > 81:
        N = 81
    N = 81 - N
    while N > 0:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if grid[i][j] != ".":
            grid[i][j] = "."
            N -= 1
    return grid

if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
