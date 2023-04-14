import random
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('My first form app')
        self.setGeometry(100, 100, 300, 300)
        self.show()


class Game:
    field = []

    def __init__(self, quantity_column):
        for c in range(quantity_column):
            column = []
            quantity_circles = random.randint(0, quantity_column - 1)

            for r in range(quantity_circles):
                column.append(random.randint(0, quantity_column))

            for r in range(quantity_circles, quantity_column):
                column.append(-1)

            self.field.append(column)

    def get_random_circle(self):
        return random.randint(0, len(self.field))

    def put_circle_in_column(self, circle, column):
        i = len(self.field) - 1

        while i != -1 and self.field[column][i] == -1:
            i -= 1
        i += 1

        self.field[column][i] = circle

    def check_field_for_extra_circles(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
