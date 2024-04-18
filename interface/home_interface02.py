# coding:utf-8
import threading
from functools import partial
from threading import Thread

from PySide6.QtCore import QSize, Qt, QThread, Signal, QRunnable, Slot, QThreadPool, QMetaObject, Q_ARG, QObject, QTimer
from PySide6.QtGui import QColor, QIcon, QDesktopServices
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect, QFileDialog
from qfluentwidgets import FluentIcon, InfoBarIcon, InfoBar, InfoBarPosition

from interface.FocusInterface_v303 import Ui_FocusInterface
from openlrc.openlrc import LRCer
import os
import shutil

from database.data_pro import FileManager

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

db_params = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123456',
    'database': 'fluent_transfer1',
    'charset': 'utf8mb4'
}


class FocusInterface(Ui_FocusInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
        self.file_manager = FileManager(db_params)

        self.thread_pool = QThreadPool()

        # set the icon of button
        self.pinButton.setIcon(FluentIcon.PIN)
        self.moreButton.setIcon(FluentIcon.MORE)
        self.startFocusButton.setIcon(FluentIcon.POWER_BUTTON)
        self.editButton.setIcon(FluentIcon.EDIT)

        #self.ToolButton1.setIcon(QIcon('ui/rsc/shasha.png'))
        self.ToolButton1.setIcon(FluentIcon.ROBOT)
        self.ToolButton1.setIconSize(QSize(60, 60))
        self.ToolButton_2.setIcon(QIcon('ui/rsc/233.png'))
        self.ToolButton_2.setIconSize(QSize(120, 120))
        self.ToolButton_3.setIcon(QIcon('ui/rsc/se.png'))
        self.ToolButton_3.setIconSize(QSize(100, 100))
        #self.ToolButton_4.setIcon(QIcon('ui/rsc/subcat.png'))
        #self.ToolButton_4.setIconSize(QSize(100, 100))
        self.ToolButton_4.setIcon(FluentIcon.ALIGNMENT)
        self.ToolButton_4.setIconSize(QSize(60, 60))

        # add shadow effect to card
        self.setShadowEffect(self.focusCard)
        self.setShadowEffect(self.progressCard)

        # set tool button function
        self.ToolButton1.clicked.connect(
            lambda: QDesktopServices.openUrl('https://yiyan.baidu.com/'))
        self.ToolButton_2.clicked.connect(
            lambda: QDesktopServices.openUrl("https://www.bilibili.com"))
        self.ToolButton_3.clicked.connect(
            lambda: QDesktopServices.openUrl("https://github.com/SubtitleEdit/subtitleedit"))
        self.ToolButton_4.clicked.connect(
            lambda: QDesktopServices.openUrl("https://srtku.com/"))
        #lambda: QDesktopServices.openUrl("https://www.subtitlecat.com/"))

        # stop progress bar
        self.loading_bar1.stop()

        # set country_selector
        # 定义语言简写和对应的中文名称
        languages = {
            'zh-hans': '简体中文',
            'zh-hant': '繁体中文',
            'en': '英语',
            'ja': '日语',
            'ko': '韩语',
            'fr': '法语',
            'ru': '俄语',
            'de': '德语',
            # 'ca': '加泰罗尼亚语',
            # 'hr': '克罗地亚语',
            # 'da': '丹麦语',
            # 'nl': '荷兰语',
            # 'fi': '芬兰语',
            # 'el': '希腊语',
            # 'it': '意大利语',
            # 'lt': '立陶宛语',
            # 'mk': '马其顿语',
            # 'nb': '挪威语（博克马尔）',
            # 'pl': '波兰语',
            # 'pt': '葡萄牙语',
            # 'ro': '罗马尼亚语',
            # 'sl': '斯洛文尼亚语',
            # 'es': '西班牙语',
            # 'sv': '瑞典语',
            # 'uk': '乌克兰语',
        }
        # 添加条目到下拉框中，设置显示的文本为中文名称，同时存储语言简写作为用户数据
        for code, name in languages.items():
            self.country_selector.addItem(name, userData=code)
        self.country_selector.currentIndexChanged.connect(self.language_changed)

        # 启动！
        self.startFocusButton.clicked.connect(self.start_calculation)

        # set open_file button function
        self.open_fileButton.clicked.connect(self.get_dict)

    def language_changed(self):
        index = self.country_selector.currentIndex()
        print(index)
        if index != -1:  # 确保有选中的条目
            code = self.country_selector.itemData(index)
            if code is not None:  # 确保用户数据不是 None
                print(f"Selected language code: {code}")
            else:
                print("No language data associated with this index.")

    def setShadowEffect(self, card: QWidget):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setColor(QColor(0, 0, 0, 15))
        shadowEffect.setBlurRadius(10)
        shadowEffect.setOffset(0, 0)
        card.setGraphicsEffect(shadowEffect)

    def createSuccessInfoBar(self):  #转译完成后生成提示条
        InfoBar.success(
            title='转译任务完成',
            content="文件已生成于根目录，请前去查看",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            # position='Custom',   # NOTE: use custom info bar manager
            duration=10000,
            parent=self
        )

    def get_dict(self):  # 文字框获取文件路径
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
        self.loading_bar1.start()
        index = self.country_selector.currentIndex()

        self.file_path = self.file_LineEdit.text()
        self.country = self.country_selector.itemData(index)
        self.trans_switch = self.translate_SwitchButton.isChecked()

        worker = WorkerTask(self.file_path, self.country, self.trans_switch)
        worker.signals.finished.connect(self.on_calculation_finished)

        self.thread_pool.start(worker)

    def on_calculation_finished(self):

        # 计算完成后的处理，更新 UI
        self.loading_bar1.stop()
        FocusInterface.createSuccessInfoBar(self)
        print("运算结束，ui更新完成")


        # 获取新的路径
        file_root, file_extension = os.path.splitext(self.file_path)
        # 更改扩展名为 .lrc
        new_file_path = file_root + '.lrc'
        # 更新实例变量 self.file_path
        self.file_path = new_file_path

        # 获取文件名
        file_name = os.path.basename(self.file_path)
        file_name = os.path.splitext(file_name)[0]

        # 添加记录到数据库
        self.file_manager.add_entry('file_records', file_name, self.country, self.file_path)

        # 删除preprocessed文件夹
        directory_path = os.path.dirname(self.file_path)
        preprocessed_folder_path = os.path.join(directory_path, 'preprocessed')
        try:
            shutil.rmtree(preprocessed_folder_path)
            print("Folder 'preprocessed' deleted successfully.")
        except Exception as e:
            print(f"Error occurred while deleting the folder 'preprocessed': {e}")

        # 在 FocusInterface 中读取环境变量
        self.default_folder_path = os.getenv('DEFAULT_FOLDER_PATH')

        if self.default_path_checker.isChecked():
            try:
                print(self.file_path, self.default_folder_path)

                shutil.move(self.file_path, self.default_folder_path)
                print("File moved to default folder successfully.")
                #生成新的file_path
                file_name = os.path.basename(self.file_path)  # 从self.file_path中提取文件名
                new_file_path = os.path.join(self.default_folder_path, file_name)  # 创建完整的目标路径

                self.file_manager.update_file_path('file_records', self.file_path, new_file_path)
            except Exception as e:
                print(f"Error occurred while moving the file: {e}")


class WorkerSignals(QObject):
    finished = Signal(str)


class WorkerTask(QRunnable):
    def __init__(self, file_path, target_lang, skip_trans):
        super().__init__()
        self.file_path = file_path
        self.target_lang = target_lang
        self.skip_trans = skip_trans
        self.signals = WorkerSignals()

    def run(self):
        # 执行lrc任务
        lrcer = LRCer()
        print(self.skip_trans)
        lrcer.run(paths=self.file_path, target_lang=self.target_lang, skip_trans=self.skip_trans)
        # 发送结束结果信号
        self.signals.finished.emit("lrc任务完成")
