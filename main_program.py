import os
import sys
from scaling import scaling
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QStatusBar

SCREEN_SIZE = [800, 450]
map_api_server = "http://static-maps.yandex.ru/1.x/"


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def getImage(self):
        map_params = {
            "ll": ",".join([self.x_coord.text(), self.y_coord.text()]),
            "spn": "0.01,0.01",
            "l": "map"
        }
        response = requests.get(map_api_server, map_params)

        if not response:
            self.statusBar().showMessage('Ошибка выполнения запроса')
            return

        self.statusBar().hide()

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        # Загрузка изображения на форму
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Большая задача по Maps API')

        # Пространство под изображение
        self.map_file = "map.png"
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

        self.x_coord, self.y_coord = QLineEdit(self), QLineEdit(self)
        self.x_coord.resize(75, 25)
        self.y_coord.resize(75, 25)
        self.x_coord.move(600, 50)
        self.y_coord.move(700, 50)

        self.x_lbl, self.y_lbl = QLabel(self), QLabel(self)
        self.x_lbl.setText("X")
        self.y_lbl.setText("Y")
        self.x_lbl.move(605, 25)
        self.y_lbl.move(705, 25)

        self.btn = QPushButton(self)
        self.btn.setText("Искать")
        self.btn.resize(100, 20)
        self.btn.move(645, 80)
        self.btn.clicked.connect(self.getImage)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())