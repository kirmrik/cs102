import random
from copy import deepcopy
from typing import List, Tuple
import pygame
from pygame.locals import *


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

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        # Создание списка клеток
        self.clist = self.cell_list()
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            # Отрисовка списка клеток
            self.draw_cell_list(self.clist)
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.update_cell_list(self.clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize: bool = True) -> List[List[int]]:
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = []
        temp = []
        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    temp.append(random.randint(0, 1))
                self.clist.append(temp[:])
                temp = []
            return self.clist
        for i in range(self.cell_width):
            temp.append(0)
        for i in range(self.cell_height):
            self.clist.append(temp[:])
        return self.clist

    def draw_cell_list(self, clist: List[List[int]]) -> None:
        """ Отображение списка клеток

        :param clist: Список клеток для отрисовки, представленный в виде матрицы
        """
        sots = self.cell_size - 1
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                pos_x = j * self.cell_size + 1
                pos_y = i * self.cell_size + 1
                if clist[i][j]:
                    cell_color = pygame.Color('green')
                else:
                    cell_color = pygame.Color('white')
                pygame.draw.rect(self.screen, cell_color, (pos_x, pos_y, sots, sots))

    def get_neighbours(self, cell: Tuple[int, int]) -> List[int]:
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        row, col = cell
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i <= self.cell_height - 1 and 0 <= j <= self.cell_width - 1:
                    neighbours.append(self.clist[i][j])
        neighbours.remove(self.clist[row][col])
        return neighbours

    def update_cell_list(self, clist: List[List[int]]) -> List[List[int]]:
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = deepcopy(clist)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                # Вычисляем количество живых соседей (Number of alive neighbours)
                noan = sum(self.get_neighbours((i, j)))
                if clist[i][j]:
                    if noan < 2 or noan > 3:
                        new_clist[i][j] = 0
                else:
                    if noan == 3:
                        new_clist[i][j] = 1
        self.clist = deepcopy(new_clist)
        return self.clist

if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
