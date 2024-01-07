# coding:utf-8
import threading
from functools import partial
from threading import Thread

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QIcon, QDesktopServices
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from qfluentwidgets import FluentIcon, InfoBarIcon, InfoBar, InfoBarPosition

from FocusInterface_v2 import Ui_FocusInterface
from openlrc import LRCer
import os

from concurrent.futures import ThreadPoolExecutor

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class FocusInterface(Ui_FocusInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)

        # set the icon of button
        self.pinButton.setIcon(FluentIcon.PIN)
        self.moreButton.setIcon(FluentIcon.MORE)
        self.startFocusButton.setIcon(FluentIcon.POWER_BUTTON)
        self.editButton.setIcon(FluentIcon.EDIT)

        self.moreTaskButton.setIcon(FluentIcon.MORE)
        self.taskIcon1.setIcon(InfoBarIcon.SUCCESS)
        self.taskIcon2.setIcon(InfoBarIcon.SUCCESS)
        self.taskIcon3.setIcon(InfoBarIcon.WARNING)
        self.taskIcon4.setIcon(InfoBarIcon.WARNING)

        self.ToolButton1.setIcon(QIcon('ui/shasha.png'))
        self.ToolButton1.setIconSize(QSize(80, 80))
        self.ToolButton_2.setIcon(QIcon('ui/233.png'))
        self.ToolButton_2.setIconSize(QSize(120, 120))
        self.ToolButton_3.setIcon(QIcon('ui/se.png'))
        self.ToolButton_3.setIconSize(QSize(100, 100))
        self.ToolButton_4.setIcon(QIcon('ui/subcat.png'))
        self.ToolButton_4.setIconSize(QSize(100, 100))

        # add shadow effect to card
        self.setShadowEffect(self.focusCard)
        self.setShadowEffect(self.progressCard)
        self.setShadowEffect(self.taskCard)

        # set tool button function
        self.ToolButton1.clicked.connect(lambda: QDesktopServices.openUrl('https://500px.com.cn/ifbook'))
        self.ToolButton_2.clicked.connect(
            lambda: QDesktopServices.openUrl("https://space.bilibili.com/22073772?spm_id_from=333.1007.0.0"))
        self.ToolButton_3.clicked.connect(
            lambda: QDesktopServices.openUrl("https://github.com/SubtitleEdit/subtitleedit"))
        self.ToolButton_4.clicked.connect(lambda: QDesktopServices.openUrl("https://www.subtitlecat.com/"))


        # progress bar
        self.loading_bar1.stop()

        self.startFocusButton.clicked.connect(self.activate_lrc)





    def setShadowEffect(self, card: QWidget):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(QColor(0, 0, 0, 15))
        shadowEffect.setBlurRadius(10)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)

    def createSuccessInfoBar(self):
        # convenient class mothod
        InfoBar.success(
            title='任务完成',
            content="文件已生成于根目录，请前去查看",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=80000,
            parent=self
        )
    def activate_lrc(self):
        FocusInterface.createSuccessInfoBar(self)
        t1 = threading.Thread(target=FocusInterface.run_lrc(self))
        t1.start()




    def run_lrc(self):
        file_target = self.file_LineEdit.text()
        target_lan = self.country_selector.text()
        skip_trans = self.translate_SwitchButton.isChecked()

        lrcer = LRCer()
        lrcer.run(paths=file_target,target_lang=str(target_lan), skip_trans=skip_trans)




