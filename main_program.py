import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

SCREEN_SIZE = [800, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Большая задача по Maps API')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

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