# coding:utf-8
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QIcon, QDesktopServices
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from qfluentwidgets import FluentIcon, InfoBarIcon

from Ui_FocusInterface_v2 import Ui_FocusInterface


class FocusInterface(Ui_FocusInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        # set the icon of button
        self.pinButton.setIcon(FluentIcon.PIN)
        self.moreButton.setIcon(FluentIcon.MORE)
        self.startFocusButton.setIcon(FluentIcon.POWER_BUTTON)
        self.editButton.setIcon(FluentIcon.EDIT)
        self.addTaskButton.setIcon(FluentIcon.ADD)
        self.moreTaskButton.setIcon(FluentIcon.MORE)
        self.taskIcon1.setIcon(InfoBarIcon.SUCCESS)
        self.taskIcon2.setIcon(InfoBarIcon.SUCCESS)
        self.taskIcon3.setIcon(InfoBarIcon.WARNING)
        self.taskIcon4.setIcon(InfoBarIcon.WARNING)


        self.ToolButton1.setIcon(QIcon('ui/shasha.png'))
        self.ToolButton1.setIconSize(QSize(80, 80))
        self.ToolButton_2.setIcon(QIcon('ui/233.png'))
        self.ToolButton_2.setIconSize(QSize(120,120))
        self.ToolButton_3.setIcon(QIcon('ui/se.png'))
        self.ToolButton_3.setIconSize(QSize(100,100))
        self.ToolButton_4.setIcon(QIcon('ui/subcat.png'))
        self.ToolButton_4.setIconSize(QSize(100,100))



        # add shadow effect to card
        self.setShadowEffect(self.focusCard)
        self.setShadowEffect(self.progressCard)
        self.setShadowEffect(self.taskCard)

        self.ToolButton1.clicked.connect(lambda : QDesktopServices.openUrl('https://500px.com.cn/ifbook'))
        self.ToolButton_2.clicked.connect(lambda: QDesktopServices.openUrl("https://space.bilibili.com/22073772?spm_id_from=333.1007.0.0"))
        self.ToolButton_3.clicked.connect(lambda: QDesktopServices.openUrl("https://github.com/SubtitleEdit/subtitleedit"))
        self.ToolButton_4.clicked.connect(lambda: QDesktopServices.openUrl("https://www.subtitlecat.com/"))

    def setShadowEffect(self, card: QWidget):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(QColor(0, 0, 0, 15))
        shadowEffect.setBlurRadius(10)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)
