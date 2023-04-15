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
    WIN = 3
    LOSE = 4


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

    def get_random_circle(self):
        return random.randint(0, self.__col_number)

    def put_circle_in_column(self, circle, column):
        if len(self.__field[column]) == self.__col_number:
            self.__state = GameStates.LOSE

        self.__field[column].append(circle)

    def check_field_for_extra_circles(self):
        pass


if __name__ == '__main__':
    d = Game(2)
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
