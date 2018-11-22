import random
from typing import List, Union
from copy import deepcopy
import pygame
from pygame.locals import *


class Cell:

    def __init__(self, row: int, col: int, state: bool = False) -> None:
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self) -> int:
        """ Вернуть состояние ячейки в виде целого числа 0 или 1"""
        if self.state:
            return 1
        return 0


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize: bool = False) -> None:
        self.nrows = nrows
        self.ncols = ncols
        self.clist = []
        if randomize:
            for i in range(nrows):
                for j in range(ncols):
                    self.clist.append(Cell(i, j, random.randint(0, 1) > 0))
        else:
            for i in range(nrows):
                for j in range(ncols):
                    self.clist.append(Cell(i, j, False))

    def get_neighbours(self, cell: List[Union[int, int, bool]]) -> List[List[Union[int, int, bool]]]:
        """ Вернуть список соседей для указанной ячейки

        :param cell: Ячейка , задана списком вида [row, col, state]
        :return: Список ячеек, смежных к ячейке cell  в сетке игры
        """
        neighbours = []
        for i in range(cell.row - 1, cell.row + 2):
            for j in range(cell.col - 1, cell.col + 2):
                if 0 <= i <= self.nrows - 1 and 0 <= j <= self.ncols - 1:
                    neighbours.append(self.clist[i * self.ncols + j])
        neighbours.remove(self.clist[cell.row * self.ncols + cell.col])
        return neighbours

    def update(self: List[List[Union[int, int, bool]]]) -> List[List[Union[int, int, bool]]]:
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param self: Игровое поле, представленное в виде списка ячеек
        :return: Обновленное игровое поле
        """
        new_clist = deepcopy(self)
        for cell in new_clist:
            noan = sum(c.is_alive() for c in self.get_neighbours(cell))
            if cell.state:
                if noan < 2 or noan > 3:
                    cell.state = 0
            else:
                if noan == 3:
                    cell.state = 1
        grid = deepcopy(new_clist)
        return grid

    def __iter__(self) -> None:
        self.ind = 0
        return self

    def __next__(self) -> List[Union[int, int, bool]]:
        """ Возвратить следующую ячейку из списка"""
        if self.ind == self.nrows * self.ncols:
            raise StopIteration
        cell = self.clist[self.ind]
        self.ind += 1
        return cell

    def __str__(self) -> str:
        """ Возвратить список ячеек в строковом формате (строки из 0 и 1)"""
        result = ""
        for cell in self:
            if cell.state:
                result += "1"
            else:
                result += "0"
            if cell.col == self.ncols - 1:
                result += "\n"
        return result

    @classmethod
    def from_file(cls, filename: str) -> List[List[Union[int, int, bool]]]:
        """ Заполнить список ячеек данными из текстового файла (строки из 0 и 1)

        :param filename: имя текстового файла
        :return: Игровое поле, представленное в виде списка ячеек
        """
        clist = []
        with open(filename) as f:
            for i, line in enumerate(f):
                line = line.rstrip('\n')
                for j, c in enumerate(line):
                    clist.append(Cell(i, j, bool(c in '1')))
        grid = cls(i + 1, j + 1, False)
        grid.clist = clist
        return grid


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_cell_list(self, clist: List[List[Union[int, int, bool]]]) -> None:
        """ Отображение списка клеток

        :param clist: Список ячеек для отрисовки
        """
        sots = self.cell_size - 1
        for cell in clist:
            pos_x = cell.col * self.cell_size + 1
            pos_y = cell.row * self.cell_size + 1
            if cell.state:
                cell_color = pygame.Color('green')
            else:
                cell_color = pygame.Color('white')
            pygame.draw.rect(self.screen, cell_color, (pos_x, pos_y, sots, sots))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        # Создание списка клеток
        # game_clist = CellList(self.cell_height, self.cell_width, randomize=True) # случайный
        game_clist = CellList.from_file('gun.txt')  # из файла
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            # Отрисовка списка клеток
            self.draw_cell_list(game_clist)
            # Выполнение одного шага игры (обновление состояния ячеек)
            game_clist = game_clist.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    game = GameOfLife(800, 340, 20)
    game.run()
