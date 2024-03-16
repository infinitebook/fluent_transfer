# coding:utf-8
import os
import sys

from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            SubtitleLabel, setFont, SplashScreen)
from qfluentwidgets import FluentIcon as FIF
from interface.focus_interface import FocusInterface
from interface.setting_interface import SettingInterface

# setting interface import
from ui.setting_common.signal_bus import signalBus
from ui.setting_common.config import cfg


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
        self.initWindow()

        # create sub interface
        self.homeInterface = FocusInterface(self)
        # 原代码：self.homeInterface = Widget('Home Interface', self)

        self.appInterface = Widget('advance transfer Interface', self)
        self.videoInterface = Widget('translator Interface', self)

        self.setting = SettingInterface(self)
        # self.setting = Widget('setting', self)

        self.libraryInterface = Widget('library Interface', self)

        self.connectSignalToSlot()

        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL, )
        self.addSubInterface(self.appInterface, FIF.SYNC, '转译')
        self.addSubInterface(self.videoInterface, FIF.LANGUAGE, '翻译')
        self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, '库', FIF.LIBRARY_FILL,
                             NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.setting, FIF.SETTING, '设置', FIF.SETTING, NavigationItemPosition.BOTTOM)

        self.navigationInterface.addItem(
            routeKey='Help',
            icon=QIcon('ui/rsc/shasha.png'),
            text='',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon('ui/rsc/logo.png'))
        self.setWindowTitle('Fluent Transfer')

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

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
    setTheme(Theme.LIGHT)

    # enable dpi scale
    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # create main window
    w = Window()
    w.show()

    app.exec()
