import random
from enum import Enum


class GameStates(Enum):
    PLAYING = 1
    LOSE = 2


class Game:

    def __init__(self, quantity_column):
        self.__field = []
        self.__col_number = quantity_column
        self.__state = GameStates.PLAYING
        for c in range(quantity_column):
            column = []
            quantity_circles = random.randint(0, quantity_column - 1)

            for r in range(quantity_circles):
                column.append(random.randint(0, quantity_column))

            self.__field.append(column)
        self.get_init_field_simple()
        self.__next_circle = self.get_random_circle()

    @property
    def field(self):
        print(self.__field)
        return self.__field

    @property
    def next_circle(self):
        return self.__next_circle

    @property
    def state(self):
        return self.__state

    def get_random_circle(self):
        return random.randint(0, self.__col_number)

    def put_circle_in_column(self, column):
        if len(self.__field[column]) == self.__col_number:
            self.__state = GameStates.LOSE

        self.__field[column].append(self.__next_circle)
        self.__next_circle = self.get_random_circle()

    def get_init_field_simple(self):
        while self.check_field_for_extra_circles():
            self.delete_extra_circles()

    def check_field_for_extra_circles(self):
        does_field_have_extra_circles = False
        # проверка по каждому ряду
        for row_index in range(self.__col_number):
            circles_num = self.count_quantity_circles_in_row(row_index)
            for col_index in range(self.__col_number):
                if row_index < len(self.__field[col_index]) and circles_num == self.__field[col_index][row_index]:
                    does_field_have_extra_circles = True
                    self.__field[col_index][row_index] = -1
        # проверка по каждой колонне
        for col_index in range(self.__col_number):
            circles_num = len(self.__field[col_index])
            for row_index in range(len(self.__field[col_index])):
                if self.__field[col_index][row_index] == circles_num:
                    does_field_have_extra_circles = True
                    self.__field[col_index][row_index] = -1

        return does_field_have_extra_circles

    def count_quantity_circles_in_row(self, row):
        count = 0

        for col in self.__field:
            if len(col) > row:
                count += 1

        return count

    def delete_extra_circles(self):
        for col_index in range(self.__col_number):
            self.__field[col_index] = list(filter(lambda circle: circle != -1, self.__field[col_index]))