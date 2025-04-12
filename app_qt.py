import sqlite3
import sys
from sqlite3 import connect

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import (
    QFont, QPainter, QColor, QPixmap, QPen, QIcon
)
from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QTableWidget, QTableWidgetItem,
    QLabel, QLineEdit, QPushButton, QComboBox,
)
from PyQt6.uic.properties import QtCore


def font(f="Consolas", s=14):
    # Это функция возвращает стиль текста
    return QFont(f, s)


class Entrance(QWidget):
    # Этот класс для входа в систему

    def __init__(self, mainwindow):
        # Проводим инициализацию
        super().__init__()
        self.initUI()
        self.mainwindow = mainwindow

    def initUI(self):
        # Этот метод для создания интерфейса
        self.setFixedSize(200, 300)
        self.setWindowTitle("  ")

        self.setStyleSheet("border-radius: 10px")
        self.setFont(font())

        self.EntranceLabel = QLabel("Вход", self)
        self.EntranceLabel.setFont(font(s=18))
        self.EntranceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.EntranceLabel.setGeometry(35, 40, 130, 30)

        self.loginLine = QLineEdit(self)
        self.loginLine.setPlaceholderText("Логин")
        self.loginLine.setStyleSheet("background-color: white")
        self.loginLine.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loginLine.setFont(font(s=12))
        self.loginLine.setGeometry(35, 100, 130, 30)

        self.passwordLine = QLineEdit(self)
        self.passwordLine.setPlaceholderText("Пароль")
        self.passwordLine.setStyleSheet("background-color: white")
        self.passwordLine.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.passwordLine.setFont(font(s=12))
        self.passwordLine.setGeometry(35, 140, 130, 30)

        self.entranceBtn = QPushButton(self)
        self.entranceBtn.setText("Далее")
        self.entranceBtn.setStyleSheet("background-color: white")
        self.entranceBtn.setFont(font(s=12))
        self.entranceBtn.setGeometry(50, 200, 100, 30)
        self.entranceBtn.clicked.connect(self.act)

    def act(self):
        login = self.loginLine.text()
        password = self.passwordLine.text()

        if not (login and password):
            return

        if self.mainwindow.cursor.execute(
            f"""SELECT login, password FROM Admins WHERE login = '{login}' and password = '{password}'"""
        ).fetchall():
            self.setVisible(False)
            self.mainwindow()

    def __call__(self):
        self.setVisible(True)


class MainWindow(QWidget):
    # Это онновное окно
    def __init__(self):
        # Проводим инициализацию
        super().__init__()
        self.login = "ADMIN"
        self.initUI()
        self.entrance = Entrance(self)

        self.con = sqlite3.connect("database.sqlite")
        self.cursor = self.con.cursor()

    def initUI(self):
        # Этот метод для создания интерфейса
        self.setFixedSize(200, 300)
        self.setWindowTitle("   ")

        self.setStyleSheet("background-color: grey")
        self.setStyleSheet("border-radius: 10px")
        self.setFont(font())

        self.menuLabel = QLabel("Меню", self)
        self.menuLabel.setFont(font(s=18))
        self.menuLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menuLabel.setGeometry(35, 30, 130, 30)

        self.сreationBtn = QPushButton(self)
        self.сreationBtn.setText("Создание")
        self.сreationBtn.setStyleSheet("background-color: white")
        self.сreationBtn.setFont(font(s=12))
        self.сreationBtn.setGeometry(40, 85, 120, 30)

        self.сhangeBtn = QPushButton(self)
        self.сhangeBtn.setText("Изменение")
        self.сhangeBtn.setStyleSheet("background-color: white")
        self.сhangeBtn.setFont(font(s=12))
        self.сhangeBtn.setGeometry(40, 130, 120, 30)

        self.removeBtn = QPushButton(self)
        self.removeBtn.setText("Удаление")
        self.removeBtn.setStyleSheet("background-color: white")
        self.removeBtn.setFont(font(s=12))
        self.removeBtn.setGeometry(40, 175, 120, 30)

        self.statBtn = QPushButton(self)
        self.statBtn.setText("Статистика")
        self.statBtn.setStyleSheet("background-color: white")
        self.statBtn.setFont(font(s=12))
        self.statBtn.setGeometry(40, 220, 120, 30)


    def update_database(self):
        self.con.commit()

    def __call__(self):
        self.setVisible(True)

    def entranceAct(self):
        self.setVisible(False)
        self.entrance()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.entranceAct()
    # wnd.setVisible(True)
    sys.excepthook = except_hook
    sys.exit(app.exec())
