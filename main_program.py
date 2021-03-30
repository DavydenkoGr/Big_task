import os
import sys
import requests
from PyQt5 import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QStatusBar

SCREEN_SIZE = [800, 450]
map_api_server = "http://static-maps.yandex.ru/1.x/"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def getImage(self):
        spn = str(0.002 * self.delta)
        print(f"{spn},{spn}")
        map_params = {
            "ll": ",".join([self.x_coord.text(), self.y_coord.text()]),
            "spn": f"{spn},{spn}",
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

        self.delta = 11

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

    def keyPressEvent(self, event):
        if self.delta > 40:
            self.delta = 40
        if self.delta < 6:
            self.delta = 6
        if str(event.key()) == "16777238":
            self.delta *= 1.5
            self.getImage()
        elif str(event.key()) == "16777239":
            self.delta *= 0.5
            self.getImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())