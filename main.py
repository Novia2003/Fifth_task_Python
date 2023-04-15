import random
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from enum import Enum


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('My first form app')
        self.setGeometry(100, 100, 300, 300)
        self.show()


class GameStates(Enum):
    NOT_STARTED = 1
    PLAYING = 2
    LOSE = 3


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

    @property
    def field(self):
        return self.__field

    def get_random_circle(self):
        return random.randint(0, self.__col_number)

    def put_circle_in_column(self, circle, column):
        if len(self.__field[column]) == self.__col_number:
            self.__state = GameStates.LOSE

        self.__field[column].append(circle)

    def check_field_for_extra_circles(self):
        # проверка по каждому ряду
        for row in range(self.__col_number):
            circles_num = self.count_quantity_circles_in_row(row)
            for col in self.__col_number:
                if row < len(self.__field[col]) and circles_num == self.__field[col][row]:
                    self.__field[col][row] = -1
        # проверка по каждой колонне
        for col in self.__col_number:
            circles_num = len(self.__field[col])
            for row in self.__field[col]:
                if self.__field[col][row] == circles_num:
                    self.__field[col][row] = -1

    def count_quantity_circles_in_row(self, row):
        count = 0

        for col in self.__field:
            if len(col) > row:
                count += 1

        return count

    def delete_extra_circles(self):
        for col in self.__col_number:
            self.__field[col] = list(filter(lambda circle: circle != -1, self.__field[col]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
