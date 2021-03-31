import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget, QComboBox, QPlainTextEdit

# Барнаул Красноармейский 133

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

        self.pc = "Почтовый индекс не найден"

        self.obj = QLineEdit(self)
        self.obj.resize(180, 25)
        self.obj.move(10, 160)

        self.address = QLabel(self)
        self.address.setText("Введите адрес")
        self.address.move(45, 135)

        self.btn1, self.btn2, self.btn3 = QPushButton(self), QPushButton(self), QPushButton(self)
        self.btn1.setText("Искать по адресу")
        self.btn2.setText("Сброс поискового результата")
        self.btn3.setText("Показать почтовый индекс")
        self.btn1.resize(150, 20)
        self.btn2.resize(180, 20)
        self.btn3.resize(180, 20)
        self.btn1.move(25, 190)
        self.btn2.move(10, 215)
        self.btn3.move(10, 240)
        self.btn1.clicked.connect(self.restart)
        self.btn2.clicked.connect(self.restart)
        self.btn3.clicked.connect(self.postal)

        self.type = QComboBox(self)
        self.type.resize(100, 20)
        self.type.move(45, 110)
        self.type.addItem("Карта")
        self.type.addItem("Спутник")
        self.type.addItem("Гибрид")

        self.adinfo = QPlainTextEdit(self)
        self.adinfo.resize(180, 80)
        self.adinfo.move(10, 10)
        self.adinfo.setDisabled(True)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)
        Map.close()

    def postal(self):
        if self.btn3.text() == "Показать почтовый индекс":
            self.btn3.setText("Спрятать почтовый индекс")
            self.adinfo.appendPlainText(self.pc)
        else:
            self.btn3.setText("Показать почтовый индекс")
            self.adinfo.undo()

    def restart(self):
        self.adinfo.clear()
        if not Map.dont_change_pos:
            Map.i, Map.rl_shift, Map.ud_shift = 0, 0, 0
        if self.sender().text() == "Искать по адресу":
            self.pt = True
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": self.obj.text(),
                "format": "json"}
            response = requests.get(geocoder_api_server, params=geocoder_params)
            json_response = response.json()
            toponym_coodrinates = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]["Point"]["pos"]
            if Map.dont_change_pos:
                Map.dont_change_pos = False
                self.ptx, self.pty = list(map(float, toponym_coodrinates.split()))
            else:
                self.x, self.y = list(map(float, toponym_coodrinates.split()))
                self.pty, self.ptx =  self.y, self.x
            self.adinfo.appendPlainText(json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"][
                "Address"]["formatted"])

            try:
                self.pc = json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]["metaDataProperty"][
                    "GeocoderMetaData"]["Address"]["postal_code"]
            except Exception:
                self.pc = "Почтовый индекс не найден"

            if self.btn3.text() == "Спрятать почтовый индекс":
                self.adinfo.appendPlainText(self.pc)
        else:
            self.pt = False
            self.pc = "Почтовый индекс не найден"
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
        if ex.pt:
            pt = ",".join([str(ex.ptx), str(ex.pty)]) + ",pm2gnm"
        else:
            pt = None
        map_params = {
            "ll": ",".join([str(float(ex.x) + self.rl_shift),
                            str(float(ex.y) + self.ud_shift)]),
            "spn": f"{spn},{spn}",
            "l": type,
            "pt": pt}
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

        self.dont_change_pos = False
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
            self.getImage()
        elif str(event.key()) == "16777236":
            self.rl_shift += float(scales[self.i]) * 2
            self.getImage()
        elif str(event.key()) == "16777235":
            self.ud_shift += float(scales[self.i])
            self.getImage()
        elif str(event.key()) == "16777237":
            self.ud_shift -= float(scales[self.i])
            self.getImage()

    def mousePressEvent(self, event):
        print(event.x(), event.y())
        x = ex.x + self.rl_shift + float(scales[self.i]) * 3.2 * (int(event.x()) - 300) / 600
        y = ex.y + self.ud_shift - float(scales[self.i]) * 1.44 * (int(event.y()) - 222.5) / 450
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": ",".join([str(x), str(y)]),
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        toponym_address = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"][
                "Address"]["formatted"]

        self.dont_change_pos = True
        ex.obj.setText(toponym_address)
        ex.btn1.click()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    Map = Map()
    ex.show()
    sys.exit(app.exec())