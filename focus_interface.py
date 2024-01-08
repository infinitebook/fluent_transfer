# coding:utf-8
import threading
from functools import partial
from threading import Thread

from PySide6.QtCore import QSize, Qt, QThread, Signal
from PySide6.QtGui import QColor, QIcon, QDesktopServices
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QFileDialog
from qfluentwidgets import FluentIcon, InfoBarIcon, InfoBar, InfoBarPosition

from FocusInterface_v2 import Ui_FocusInterface
from openlrc import LRCer
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

global file_path,country,trans_switch




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
        # 启动！
        self.startFocusButton.clicked.connect(self.start_calculation)
        # set open_file button function
        self.open_fileButton.clicked.connect(self.get_dict)

    def setShadowEffect(self, card: QWidget):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(QColor(0, 0, 0, 15))
        shadowEffect.setBlurRadius(10)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)

    def createSuccessInfoBar(self):
        # convenient class mothod
        InfoBar.success(
            title='转译任务完成',
            content="文件已生成于根目录，请前去查看",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=30000,
            parent=self
        )

    def get_dict(self):  # 获取文件路径
        file_dict = QFileDialog.getOpenFileName(parent=self, caption="请选择文件路径",
                                                filter=(
                                                    "All Files (*.*);;Videos (*.mp4 *.avi *.mpeg);; Audios (*.mp3 *.wav *.aac "))
        # 通过eval将字符串转换为元组
        path_tuple = eval(str(file_dict))
        # 获取路径部分
        path = path_tuple[0]
        # 获取纯路径
        pure_path = os.path.normpath(path)
        self.file_LineEdit.setText(pure_path)

    def start_calculation(self):
        # 创建并启动线程
        global file_path,country,trans_switch
        self.loading_bar1.start()

        file_path = self.file_LineEdit.text()
        country=self.country_selector.text()
        trans_switch=str(self.translate_SwitchButton.isChecked())
        self.worker_thread = WorkerThread()
        self.worker_thread.finished_signal.connect(self.on_calculation_finished)
        self.worker_thread.start()

    def on_calculation_finished(self, result):
        # 计算完成后的处理，更新 UI
        self.loading_bar1.stop()
        FocusInterface.createSuccessInfoBar(self)
        print(result)
        self.worker_thread.quit()
        self.worker_thread.wait()


class WorkerThread(QThread):
    finished_signal = Signal(str)
    def run(self):
        # 执行lrc任务
        result = self.perform_calculation()

        # 发送结束结果信号
        self.finished_signal.emit(result)

    def perform_calculation(self):
        # lrc计算
        file_target = file_path
        target_lan = country
        skip_trans = trans_switch

        lrcer = LRCer()
        lrcer.run(paths=file_target, target_lang=str(target_lan), skip_trans=skip_trans)

