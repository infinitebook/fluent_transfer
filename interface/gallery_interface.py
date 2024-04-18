# coding:utf-8
from PySide6.QtCore import Qt, Signal, QUrl, QEvent
from PySide6.QtGui import QDesktopServices, QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon,
                            isDarkTheme, IconWidget, Theme, ToolTipFilter, TitleLabel, CaptionLabel,
                            StrongBodyLabel, BodyLabel, toggleTheme)
from ui.setting_common.style_sheet import StyleSheet
from ui.setting_common.signal_bus import signalBus


class SeparatorWidget(QWidget):
    """ Seperator widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(6, 16)

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen(1)
        pen.setCosmetic(True)
        c = QColor(255, 255, 255, 21) if isDarkTheme() else QColor(0, 0, 0, 15)
        pen.setColor(c)
        painter.setPen(pen)

        x = self.width() // 2
        painter.drawLine(x, 0, x, self.height())


class ToolBar(QWidget):
    """ Tool bar """

    def __init__(self, title, subtitle, parent=None):
        print("Initializing ToolBar")
        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)

        self.delete_Button = PushButton(
            self.tr('删除文件'), self, FluentIcon.DELETE) #删除文件

        self.refresh_Button=ToolButton(FluentIcon.SYNC, self) #刷新
        self.separator = SeparatorWidget(self)
        self.open_file_path_Button = ToolButton(FluentIcon.FOLDER, self)       #打开目录
        self.open_file_Button = ToolButton(FluentIcon.RIGHT_ARROW, self) #打开文件

        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(138)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addWidget(self.delete_Button, 0, Qt.AlignLeft)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.refresh_Button, 0, Qt.AlignRight)
        self.buttonLayout.addWidget(self.separator, 0, Qt.AlignRight)
        self.buttonLayout.addWidget(self.open_file_path_Button, 0, Qt.AlignRight)
        self.buttonLayout.addWidget(self.open_file_Button, 0, Qt.AlignRight)
        self.buttonLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.refresh_Button.installEventFilter(ToolTipFilter(self.refresh_Button))
        self.open_file_path_Button.installEventFilter(ToolTipFilter(self.open_file_path_Button))
        self.open_file_Button.installEventFilter(
            ToolTipFilter(self.open_file_Button))
        self.refresh_Button.setToolTip(self.tr('刷新'))
        self.open_file_path_Button.setToolTip(self.tr('打开所在文件夹'))
        self.open_file_Button.setToolTip(self.tr('打开文件'))

        self.subtitleLabel.setTextColor(QColor(96, 96, 96), QColor(216, 216, 216))


class ExampleCard(QWidget):
    """ Example card """

    def __init__(self, title, widget: QWidget,  stretch=0, parent=None):
        super().__init__(parent=parent)
        self.widget = widget
        self.stretch = stretch

        self.titleLabel = StrongBodyLabel(title, self)
        self.card = QFrame(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.topLayout = QHBoxLayout()

        self.__initWidget()

    def __initWidget(self):
        self.__initLayout()

        self.card.setObjectName('card')

    def __initLayout(self):
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.cardLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.topLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setContentsMargins(12, 12, 12, 12)

        self.cardLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.card, 0, Qt.AlignTop)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.cardLayout.setSpacing(0)
        self.cardLayout.setAlignment(Qt.AlignTop)
        self.cardLayout.addLayout(self.topLayout, 0)

        self.widget.setParent(self.card)
        self.topLayout.addWidget(self.widget)
        if self.stretch == 0:
            self.topLayout.addStretch(1)

        self.widget.show()


class GalleryInterface(ScrollArea):
    """ Gallery interface """

    def __init__(self, title: str, subtitle: str, parent=None):
        """
        Parameters
        ----------
        title: str
            The title of gallery

        subtitle: str
            The subtitle of gallery

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = ToolBar(title, subtitle, self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.view.setObjectName('view')
        StyleSheet.GALLERY_INTERFACE.apply(self)

    def addExampleCard(self, title, widget,  stretch=0):
        card = ExampleCard(title, widget, stretch, self.view)
        self.vBoxLayout.addWidget(card, 0, Qt.AlignTop)
        return card

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())

    def connectDeleteButton(self,callback):
        self.toolBar.delete_Button.clicked.connect(callback)
    def connectThemeButton(self,callback):
        self.toolBar.refresh_Button.clicked.connect(callback)
    def connectSupportButton(self, callback):
        self.toolBar.open_file_path_Button.clicked.connect(callback)
    def connectOpenfileButton(self,callback):
        self.toolBar.open_file_Button.clicked.connect(callback)
