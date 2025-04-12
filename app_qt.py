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
        self.initUI()
        self.entrance = Entrance(self)
        self.pushwindow = None

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
        self.сreationBtn.clicked.connect(self.pushwindowAct)

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

    def pushwindowAct(self):
        # self.setVisible(False)
        self.pushwindow = PushWindow(self)
        self.pushwindow()

class PushWindow(QWidget):
    def __init__(self, mainwindow):
        # Проводим инициализацию
        super().__init__()

        self.initUI()
        self.mainwindow = mainwindow

    def initUI(self):
        # Этот метод для создания интерфейса
        self.setFixedSize(600, 300)
        self.setWindowTitle("Push")

        self.setStyleSheet("background-color: grey")
        self.setStyleSheet("border-radius: 10px")
        self.setFont(font())

        self.head = QLabel("Добавить", self)
        self.head.setFont(font(s=18))
        self.head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.head.setGeometry(35, 30, 130, 30)

        self.sp = QComboBox(self)
        self.sp.addItems(["ученик", "родитель", "учитель", "воспитатель"])
        self.sp.setStyleSheet("background-color: white")
        self.sp.setFont(font(s=12))
        self.sp.setGeometry(40, 85, 120, 30)
        self.sp.currentTextChanged.connect(self.act)

        ## Student
        self.id_student = QLineEdit(self)
        self.id_student.setPlaceholderText("id")
        self.id_student.setStyleSheet("background-color: white")
        self.id_student.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id_student.setFont(font(s=12))
        self.id_student.setGeometry(140, 85, 130, 30)
        self.id_student.setVisible(False)

        self.surname_student = QLineEdit(self)
        self.surname_student.setPlaceholderText("surname")
        self.surname_student.setStyleSheet("background-color: white")
        self.surname_student.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.surname_student.setFont(font(s=12))
        self.surname_student.setGeometry(140, 120, 130, 30)
        self.surname_student.setVisible(False)

        self.fathername_student = QLineEdit(self)
        self.fathername_student.setPlaceholderText("fathername")
        self.fathername_student.setStyleSheet("background-color: white")
        self.fathername_student.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fathername_student.setFont(font(s=12))
        self.fathername_student.setGeometry(140, 155, 130, 30)
        self.fathername_student.setVisible(False)

        self.class_student = QLineEdit(self)
        self.class_student.setPlaceholderText("class")
        self.class_student.setStyleSheet("background-color: white")
        self.class_student.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.class_student.setFont(font(s=12))
        self.class_student.setGeometry(280, 85, 130, 30)
        self.class_student.setVisible(False)

        self.tg_id_student = QLineEdit(self)
        self.tg_id_student.setPlaceholderText("tg_id")
        self.tg_id_student.setStyleSheet("background-color: white")
        self.tg_id_student.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tg_id_student.setFont(font(s=12))
        self.tg_id_student.setGeometry(280, 120, 130, 30)
        self.tg_id_student.setVisible(False)

        ## Parent
        self.id_parent = QLineEdit(self)
        self.id_parent.setPlaceholderText("id")
        self.id_parent.setStyleSheet("background-color: white")
        self.id_parent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id_parent.setFont(font(s=12))
        self.id_parent.setGeometry(140, 85, 130, 30)
        self.id_parent.setVisible(False)

        self.son_parent = QLineEdit(self)
        self.son_parent.setPlaceholderText("son")
        self.son_parent.setStyleSheet("background-color: white")
        self.son_parent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.son_parent.setFont(font(s=12))
        self.son_parent.setGeometry(140, 120, 130, 30)
        self.son_parent.setVisible(False)

        self.tg_id_parent = QLineEdit(self)
        self.tg_id_parent.setPlaceholderText("tg_id")
        self.tg_id_parent.setStyleSheet("background-color: white")
        self.tg_id_parent.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tg_id_parent.setFont(font(s=12))
        self.tg_id_parent.setGeometry(140, 155, 130, 30)
        self.tg_id_parent.setVisible(False)

        ## Abuy
        self.id_abuy = QLineEdit(self)
        self.id_abuy.setPlaceholderText("id")
        self.id_abuy.setStyleSheet("background-color: white")
        self.id_abuy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id_abuy.setFont(font(s=12))
        self.id_abuy.setGeometry(140, 85, 130, 30)
        self.id_abuy.setVisible(False)

        self.surname_abuy = QLineEdit(self)
        self.surname_abuy = QLineEdit(self)
        self.surname_abuy.setPlaceholderText("surname")
        self.surname_abuy.setStyleSheet("background-color: white")
        self.surname_abuy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.surname_abuy.setFont(font(s=12))
        self.surname_abuy.setGeometry(140, 120, 130, 30)
        self.surname_abuy.setVisible(False)

        self.fathername_abuy = QLineEdit(self)
        self.fathername_abuy.setPlaceholderText("fathername")
        self.fathername_abuy.setStyleSheet("background-color: white")
        self.fathername_abuy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fathername_abuy.setFont(font(s=12))
        self.fathername_abuy.setGeometry(140, 155, 130, 30)
        self.fathername_abuy.setVisible(False)

        self.tg_id_abuy = QLineEdit(self)
        self.tg_id_abuy.setPlaceholderText("tg_id")
        self.tg_id_abuy.setStyleSheet("background-color: white")
        self.tg_id_abuy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tg_id_abuy.setFont(font(s=12))
        self.tg_id_abuy.setGeometry(280, 85, 130, 30)
        self.tg_id_abuy.setVisible(False)

        ## Teacher
        self.id_teacher = QLineEdit(self)
        self.id_teacher.setPlaceholderText("id")
        self.id_teacher.setStyleSheet("background-color: white")
        self.id_teacher.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id_teacher.setFont(font(s=12))
        self.id_teacher.setGeometry(140, 85, 130, 30)
        self.id_teacher.setVisible(False)

        self.name_teacher = QLineEdit(self)
        self.name_teacher.setPlaceholderText("name")
        self.name_teacher.setStyleSheet("background-color: white")
        self.name_teacher.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_teacher.setFont(font(s=12))
        self.name_teacher.setGeometry(140, 120, 130, 30)
        self.name_teacher.setVisible(False)

        self.surname_teacher = QLineEdit(self)
        self.surname_teacher.setPlaceholderText("surname")
        self.surname_teacher.setStyleSheet("background-color: white")
        self.surname_teacher.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.surname_teacher.setFont(font(s=12))
        self.surname_teacher.setGeometry(140, 155, 130, 30)
        self.surname_teacher.setVisible(False)

        self.fathername_teacher = QLineEdit(self)
        self.fathername_teacher.setPlaceholderText("fathername")
        self.fathername_teacher.setStyleSheet("background-color: white")
        self.fathername_teacher.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fathername_teacher.setFont(font(s=12))
        self.fathername_teacher.setGeometry(280, 85, 130, 30)
        self.fathername_teacher.setVisible(False)

        self.tg_id_teacher = QLineEdit(self)
        self.tg_id_teacher.setPlaceholderText("tg_id")
        self.tg_id_teacher.setStyleSheet("background-color: white")
        self.tg_id_teacher.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tg_id_teacher.setFont(font(s=12))
        self.tg_id_teacher.setGeometry(280, 120, 130, 30)
        self.tg_id_teacher.setVisible(False)

        self.subject_teacher = QLineEdit(self)
        self.subject_teacher.setPlaceholderText("subject")
        self.subject_teacher.setStyleSheet("background-color: white")
        self.subject_teacher.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subject_teacher.setFont(font(s=12))
        self.subject_teacher.setGeometry(280, 155, 130, 30)
        self.subject_teacher.setVisible(False)

        self.pushBtn = QPushButton("12222")
        self.subject_teacher.setStyleSheet("background-color: white")
        self.subject_teacher.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subject_teacher.setFont(font(s=12))
        self.subject_teacher.setGeometry(0, 0, 130, 30)


    def act(self):
        ## Student
        self.id_student.setVisible(False)
        self.surname_student.setVisible(False)
        self.fathername_student.setVisible(False)
        self.class_student.setVisible(False)
        self.tg_id_student.setVisible(False)

        ## Parent
        self.id_parent.setVisible(False)
        self.son_parent.setVisible(False)
        self.tg_id_parent.setVisible(False)

        ## Abuy
        self.id_abuy.setVisible(False)
        self.surname_abuy.setVisible(False)
        self.fathername_abuy.setVisible(False)
        self.tg_id_abuy.setVisible(False)

        ## Teacher
        self.id_teacher.setVisible(False)
        self.name_teacher.setVisible(False)
        self.surname_teacher.setVisible(False)
        self.fathername_teacher.setVisible(False)
        self.tg_id_teacher.setVisible(False)
        self.subject_teacher.setVisible(False)

        if self.sp.currentText() == "ученик":
            self.id_student.setVisible(True)
            self.surname_student.setVisible(True)
            self.fathername_student.setVisible(True)
            self.class_student.setVisible(True)
            self.tg_id_student.setVisible(True)

        if self.sp.currentText() == "родитель":
            self.id_parent.setVisible(True)
            self.son_parent.setVisible(True)
            self.tg_id_parent.setVisible(True)

        if self.sp.currentText() == "воспитатель":
            self.id_abuy.setVisible(True)
            self.surname_abuy.setVisible(True)
            self.fathername_abuy.setVisible(True)
            self.tg_id_abuy.setVisible(True)

        if self.sp.currentText() == "учитель":
            self.id_teacher.setVisible(True)
            self.name_teacher.setVisible(True)
            self.surname_teacher.setVisible(True)
            self.fathername_teacher.setVisible(True)
            self.tg_id_teacher.setVisible(True)
            self.subject_teacher.setVisible(True)


    def __call__(self):
        self.setVisible(True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.entranceAct()
    # wnd.setVisible(True)
    sys.excepthook = except_hook
    sys.exit(app.exec())
