import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget, QComboBox

# 37.530887 55.703118

SCREEN_SIZE = [600, 450]
scales = ["0.002", "0.005", "0.01", "0.05", "0.1"]
map_api_server = "http://static-maps.yandex.ru/1.x/"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 200, 450)
        self.setWindowTitle('Окно управления')

        self.x_coord, self.y_coord = QLineEdit(self), QLineEdit(self)
        self.x_coord.resize(75, 25)
        self.y_coord.resize(75, 25)
        self.x_coord.move(0, 50)
        self.y_coord.move(100, 50)

        self.x_lbl, self.y_lbl = QLabel(self), QLabel(self)
        self.x_lbl.setText("X")
        self.y_lbl.setText("Y")
        self.x_lbl.move(5, 25)
        self.y_lbl.move(105, 25)

        self.btn = QPushButton(self)
        self.btn.setText("Искать")
        self.btn.resize(100, 20)
        self.btn.move(45, 80)
        self.btn.clicked.connect(self.restart)

        self.type = QComboBox(self)
        self.type.resize(100, 20)
        self.type.move(45, 110)
        self.type.addItem("Карта")
        self.type.addItem("Спутник")
        self.type.addItem("Гибрид")

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)
        Map.close()

    def restart(self):
        self.i, self.rl_shift, self.ud_shift = 0, 0, 0
        Map.show()
        Map.getImage()


class Map(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def getImage(self):
        spn = scales[self.i]
        if ex.type.currentText() == "Карта":
            type = "map"
        elif ex.type.currentText() == "Спутник":
            type = "sat"
        else:
            type = "skl"

        map_params = {
            "ll": ",".join([str(float(ex.x_coord.text()) + self.rl_shift),
                            str(float(ex.y_coord.text()) + self.ud_shift)]),
            "spn": f"{spn},{spn}",
            "l": type
        }

        response = requests.get(map_api_server, map_params)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        # Загрузка изображения на форму
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def initUI(self):
        self.setGeometry(300, 100, *SCREEN_SIZE)
        self.setWindowTitle('Большая задача по Maps API')

        self.i = 0
        self.rl_shift = 0
        self.ud_shift = 0

        # Пространство под изображение
        self.map_file = "map.png"
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)
        ex.close()

    def keyPressEvent(self, event):
        if str(event.key()) == "16777238":
            if self.i != len(scales) - 1:
                self.i += 1
            self.getImage()
        elif str(event.key()) == "16777239":
            if self.i != 0:
                self.i -= 1
            self.getImage()
        elif str(event.key()) == "16777234":
            self.rl_shift -= float(scales[self.i]) * 2
            if float(ex.x_coord.text()) + self.rl_shift not in range(-180, 180):
                self.rl_shift += float(scales[self.i]) * 2
            self.getImage()
        elif str(event.key()) == "16777236":
            self.rl_shift += float(scales[self.i]) * 2
            if float(ex.x_coord.text()) + self.rl_shift not in range(-180, 180):
                self.rl_shift -= float(scales[self.i]) * 2
            self.getImage()
        elif str(event.key()) == "16777235":
            self.ud_shift += float(scales[self.i])
            if float(ex.y_coord.text()) + self.ud_shift not in range(-90, 90):
                self.ud_shift -= float(scales[self.i]) * 2
            self.getImage()
        elif str(event.key()) == "16777237":
            self.ud_shift -= float(scales[self.i])
            if float(ex.y_coord.text()) + self.ud_shift not in range(-90, 90):
                self.ud_shift += float(scales[self.i]) * 2
            self.getImage()
        print(event.key())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    Map = Map()
    ex.show()
    sys.exit(app.exec())