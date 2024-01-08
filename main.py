# coding:utf-8
import sys

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout,QWidget
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF
from focus_interface import FocusInterface



class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))



class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.homeInterface = FocusInterface(self)
        # 原代码：self.homeInterface = Widget('Home Interface', self)
        self.appInterface = Widget('advance transfer Interface', self)
        self.videoInterface = Widget('translator Interface', self)
        self.setting = Widget('setting', self)
        self.libraryInterface = Widget('library Interface', self)


        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL, )
        self.addSubInterface(self.appInterface, FIF.SYNC, '转译')
        self.addSubInterface(self.videoInterface, FIF.LANGUAGE, '翻译')
        self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, '库', FIF.LIBRARY_FILL,NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.setting,FIF.SETTING,'设置',FIF.SETTING,NavigationItemPosition.BOTTOM)

        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('ui/logo.png'))
        self.setWindowTitle('Fluent Transfer')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showMessageBox(self):
        w = MessageBox(
            'Fluent_transfer✨',
            'the code is lisensed under GNU General Public License v3\n'
            '了解更多，关注github page🤣🤣\n\n'
            'Copyright © 2024 by infinitebook.',
           self
        )
        w.yesButton.setText('github page')
        w.cancelButton.setText('ok')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://space.bilibili.com/22073772?spm_id_from=333.1007.0.0"))


if __name__ == '__main__':
    setTheme(Theme.AUTO)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
