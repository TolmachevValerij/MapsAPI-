import os
import sys

import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class MyMap(QMainWindow):
    def __init__(self):
        super().__init__()
        self.x, self.y, self.masht = '67.530887', '55.703118', '0.002'
        self.vid = 'map'
        uic.loadUi('3.ui', self)
        self.pushButton.clicked.connect(self.setImageToPixmap)
        # 37.530887, 55.703118
        self.map_request_str = ''
        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                            self.y, '&spn=', self.masht, ',', self.masht, '&l=', self.vid]
        self.setImageToPixmap()
        self.setSelfFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            try:
                self.mashtab.setPlainText(str(float(self.mashtab.toPlainText()) + 0.01))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_PageDown:
            try:
                self.mashtab.setPlainText(str(float(self.mashtab.toPlainText()) - 0.01))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Up:
            print(2)
            try:
                self.edit_y.setPlainText(str(float(self.edit_y.toPlainText()) -
                                             2 * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Down:
            print(1)
            try:
                self.edit_y.setPlainText(str(float(self.edit_y.toPlainText()) +
                                             2 * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Right:
            try:
                self.edit_x.setPlainText(str(float(self.edit_x.toPlainText()) +
                                             2 * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        if event.key() == Qt.Key_Left:
            try:
                self.edit_x.setPlainText(str(float(self.edit_x.toPlainText()) -
                                             2 * float(self.mashtab.toPlainText())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)

    def getImage(self):
        self.x = self.edit_x.toPlainText().strip()
        self.y = self.edit_y.toPlainText().strip()
        self.masht = self.mashtab.toPlainText().strip()
        if self.layer.currentIndex() == 0:
            self.vid = 'sat'
        if self.layer.currentIndex() == 1:
            self.vid = 'map'
        if self.layer.currentIndex() == 2:
            self.vid = 'skl'
        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                            self.y, '&spn=', self.masht, ',', self.masht, '&l=', self.vid]
        self.map_request_str = ''.join(self.map_request)
        response = requests.get(self.map_request_str)
        if not response:
            return str('Ошибка выполнения запроса:' + '\n' + 'Http статус:' +
                       str(response.status_code) + '(' + str(response.reason) + ')')
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        # Запишем полученное изображение в файл.
        if self.layer.currentIndex() > 0:
            self.map_file = "map.png"
        else:
            self.map_file = "map.jpg"
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
            win = WarningWindow(self, is_all_secc)
            win.show()
        self.setSelfFocus()

    def setSelfFocus(self):
        print('Focus Setted')
        self.setFocusPolicy(Qt.StrongFocus)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)
class WarningWindow(QMainWindow):
    def __init__(self, main, text):
        super().__init__(main)
        self.setGeometry(50, 50, 500, 500)
        self.warning = QLabel(self)
        self.warning.setText(text)
        self.warning.resize(self.warning.sizeHint())
        self.warning.move(250 - self.warning.width() // 2, 250 - self.warning.height() // 2)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMap()
    ex.show()
    sys.exit(app.exec())