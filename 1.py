import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic


class APIMap(QWidget):
    def __init__(self):
        super().__init__()
        self.x, self.y, self.m = '65.537696', '57.151173', '0.002'
        uic.loadUi('maps.ui', self)
        self.pushButton.clicked.connect(self.setImageToPixmap)
        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',', self.y,
                            '&spn=', self.m, ',', self.m, '&l=map']

    def getImage(self):
        self.x = self.edit_x.toPlainText()
        self.y = self.edit_y.toPlainText()
        self.m = self.mashtab.toPlainText()
        self.map_request = ''.join(['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                                    self.y, '&spn=', self.m, ',', self.m, '&l=map'])
        response = requests.get(self.map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return "Ошибка выполнения запроса:" + '\n' + "Http статус:", response.status_code, "(", response.reason, ")"
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        return 'успех'
    def setImageToPixmap(self):
        is_all_secc = self.getImage()
        if is_all_secc == 'успех':
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        else:
            self.image.setText(is_all_secc)
    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = APIMap()
    ex.show()
    sys.exit(app.exec())
