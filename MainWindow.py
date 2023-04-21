from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QBrush, QColor, QPixmap, QPainter, QPen, QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QTableWidgetItem, QLabel, QMessageBox, qApp, QApplication, \
    QDialog
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QHeaderView

from Game import Game, GameStates
from first import Ui_MainWindow as MainWindowUI
from Rules import Ui_Dialog as Rules
from settings import Ui_Dialog as Settings


class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self):
        super().__init__()
        self.third_window = None
        self.second_window = None
        self.setupUi(self)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)
        self._game = None
        self.start(10)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('Меню')
        open_window_action = QtWidgets.QAction('Правила игры', self)
        open_window_action.triggered.connect(self.open_rules_window)
        file_menu.addAction(open_window_action)
        open_window_action = QtWidgets.QAction('Поменять размеры поля', self)
        open_window_action.triggered.connect(self.open_settings_window)
        file_menu.addAction(open_window_action)

    def open_rules_window(self):
        self.second_window = RulesWindow()
        self.second_window.show()

    def open_settings_window(self):
        self.third_window = SettingsWindow()
        self.third_window.rejected.connect(self.handle_settings_window_closed)
        self.third_window.show()

    def handle_settings_window_closed(self):
        self.start(Field_size.size)

    def start(self, column_number):
        self._game = Game(column_number)
        self.fill_field(self._game.field)
        self.fill_field_widget()

        self.tableWidget.setMouseTracking(True)
        self.tableWidget.cellClicked.connect(self.on_cell_clicked)
        self.tableWidget.cellEntered.connect(self.on_cell_entered)
        self.tableWidget.setCurrentCell(-1, -1)

    def fill_field_widget(self):
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                label = QLabel()
                self.tableWidget.setCellWidget(row, col, label)

    def on_cell_clicked(self, row, col):
        self._game.put_circle_in_column(col)

        # for col_index in range(self.tableWidget.columnCount()):
        #     self.tableWidget.takeItem(0, col_index)

        self.fill_field(self._game.field)

        if self._game.state == GameStates.LOSE:
            self.show_game_over_dialog()
        else:
            QTimer.singleShot(3000, self.check_for_chain)

    def check_for_chain(self):
        while self._game.check_field_for_extra_circles():
            self._game.delete_extra_circles()
        self.fill_field(self._game.field)

    def on_cell_entered(self, row, col):
        cell_widget = self.tableWidget.cellWidget(row, col)
        if cell_widget:
            for col_index in range(self.tableWidget.columnCount()):
                if col_index == col:
                    self.tableWidget.setItem(0, col_index, self.get_item(self._game.next_circle))
                else:
                    self.tableWidget.takeItem(0, col_index)
        self.tableWidget.update()

    def fill_field(self, field):
        self.clear_field()
        self.tableWidget.setRowCount(len(field) + 1)
        self.tableWidget.setColumnCount(len(field))

        for col_index in range(len(field)):
            for row_index in range(len(field[col_index])):
                number = field[col_index][row_index]
                item = self.get_item(number)

                self.tableWidget.setItem(len(field) - row_index, col_index, item)

        self.tableWidget.update()

    def clear_field(self):
        for row in range(self.tableWidget.rowCount()):
            for col in range(self.tableWidget.columnCount()):
                self.tableWidget.takeItem(row, col)

    def get_item(self, number):
        item = QTableWidgetItem()
        # item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        row_height = self.tableWidget.rowHeight(0)  # высота строки
        col_width = self.tableWidget.columnWidth(0)  # ширина столбца
        cell_size = QtCore.QSize(col_width, row_height)  # размер ячейки
        pixmap = QPixmap(cell_size)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        circle_color = self.get_color(number)
        brush = QBrush(QColor(circle_color))
        painter.setBrush(brush)
        rect_width = col_width - 1  # вычитаем 1, чтобы круг не выходил за пределы ячейки
        rect_height = row_height - 1
        rect_x = (col_width - rect_width) / 2
        rect_y = (row_height - rect_height) / 2
        rect = QtCore.QRectF(rect_x, rect_y, rect_width, rect_height)
        painter.drawEllipse(rect)
        painter.setPen(QPen(self.get_contrast_color(circle_color), 0))
        font = QFont('Arial', 26)
        painter.setFont(font)
        if number != 0:
            painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter, str(number))
        painter.end()
        item.setIcon(QIcon(pixmap))
        return item

    def get_contrast_color(self, color_name):
        color = QColor(color_name)
        brightness = 0.2126 * color.red() + 0.7152 * color.green() + 0.0722 * color.blue()

        if brightness > 255 / 2:
            return QtCore.Qt.black
        else:
            return QtCore.Qt.white

    def create_circle_item(self, number, color):
        item = QTableWidgetItem()
        if number != 0:
            item.setText(str(number))
        brush = QBrush(QColor(color))
        item.setBackground(brush)
        item.setForeground(QBrush(QtCore.Qt.white))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item

    @staticmethod
    def get_color(number):
        colors_dict = {
            0: 'gray',
            1: 'orange',
            2: 'yellow',
            3: 'green',
            4: 'blue',
            5: 'purple',
            6: 'pink',
            7: 'brown',
            8: 'red',
            9: 'beige',
            10: 'turquoise'
        }

        return colors_dict[number]

    def show_game_over_dialog(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Игра окончена")
        msg_box.setText('''Вы проиграли или захотели побыстрее закончить. 
                            Желаете продолжить?''')
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Ok)

        ok_button = msg_box.button(QMessageBox.Ok)
        ok_button.setText("ДА")

        cancel_button = msg_box.button(QMessageBox.Cancel)
        cancel_button.setText("НЕТ!!!!")
        msg_box.buttonClicked.connect(self.game_over_action)
        msg_box.exec_()

    def game_over_action(self, button):
        if button.text() == "ДА":
            self.start(10)
        elif button.text() == "НЕТ!!!!":
            qApp.quit()


class RulesWindow(QtWidgets.QMainWindow, Rules):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class SettingsWindow(QtWidgets.QDialog, Settings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.read_spinbox_value)

    def read_spinbox_value(self):
        value = self.spinBox.value()
        Field_size.size = value


class Field_size:
    size = 10

    @staticmethod
    def reset_size():
        Field_size.size = 4
