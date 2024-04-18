# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FocusInterface_v2.1.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLayout,
    QSizePolicy, QSpacerItem, QWidget)

from qfluentwidgets import (BodyLabel, CardWidget, CheckBox, ComboBox,
    HyperlinkButton, IconWidget, IndeterminateProgressBar, LineEdit,
    PrimaryPushButton, PushButton, StrongBodyLabel, SubtitleLabel,
    SwitchButton, ToolButton, TransparentToolButton)


class Ui_FocusInterface(object):
    def setupUi(self, FocusInterface):
        if not FocusInterface.objectName():
            FocusInterface.setObjectName(u"FocusInterface")
        FocusInterface.resize(958, 752)
        self.horizontalLayout_3 = QHBoxLayout(FocusInterface)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(20, 15, 20, 15)
        self.progressCard = CardWidget(FocusInterface)
        self.progressCard.setObjectName(u"progressCard")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressCard.sizePolicy().hasHeightForWidth())
        self.progressCard.setSizePolicy(sizePolicy)
        self.progressCard.setMinimumSize(QSize(380, 410))
        self.progressCard.setMaximumSize(QSize(600, 410))
        self.gridLayout_5 = QGridLayout(self.progressCard)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalSpacer_13 = QSpacerItem(31, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_13, 3, 3, 1, 1)

        self.ToolButton_4 = ToolButton(self.progressCard)
        self.ToolButton_4.setObjectName(u"ToolButton_4")
        self.ToolButton_4.setMinimumSize(QSize(131, 141))

        self.gridLayout_5.addWidget(self.ToolButton_4, 4, 4, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, -1, -1, -1)
        self.progressIcon = IconWidget(self.progressCard)
        self.progressIcon.setObjectName(u"progressIcon")
        self.progressIcon.setMinimumSize(QSize(18, 18))
        self.progressIcon.setMaximumSize(QSize(18, 18))
        icon = QIcon()
        icon.addFile(u":/images/tips.png", QSize(), QIcon.Normal, QIcon.Off)
        self.progressIcon.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.progressIcon)

        self.horizontalSpacer_8 = QSpacerItem(2, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)

        self.dailyProgressLabel = StrongBodyLabel(self.progressCard)
        self.dailyProgressLabel.setObjectName(u"dailyProgressLabel")

        self.horizontalLayout_4.addWidget(self.dailyProgressLabel)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_9)

        self.editButton = TransparentToolButton(self.progressCard)
        self.editButton.setObjectName(u"editButton")

        self.horizontalLayout_4.addWidget(self.editButton, 0, Qt.AlignRight)


        self.gridLayout_5.addLayout(self.horizontalLayout_4, 0, 0, 1, 6)

        self.ToolButton_2 = ToolButton(self.progressCard)
        self.ToolButton_2.setObjectName(u"ToolButton_2")
        self.ToolButton_2.setMinimumSize(QSize(131, 141))

        self.gridLayout_5.addWidget(self.ToolButton_2, 3, 4, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_5, 1, 3, 1, 1)

        self.ToolButton_3 = ToolButton(self.progressCard)
        self.ToolButton_3.setObjectName(u"ToolButton_3")
        self.ToolButton_3.setMinimumSize(QSize(131, 141))

        self.gridLayout_5.addWidget(self.ToolButton_3, 4, 2, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_15, 3, 5, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(31, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_14, 4, 3, 1, 1)

        self.ToolButton1 = ToolButton(self.progressCard)
        self.ToolButton1.setObjectName(u"ToolButton1")
        self.ToolButton1.setMinimumSize(QSize(131, 141))

        self.gridLayout_5.addWidget(self.ToolButton1, 3, 2, 1, 1)

        self.horizontalSpacer_17 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_17, 4, 5, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_16, 3, 0, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_9, 5, 3, 1, 1)

        self.horizontalSpacer_18 = QSpacerItem(30, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_18, 4, 0, 1, 1)


        self.gridLayout.addWidget(self.progressCard, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.focusCard = CardWidget(FocusInterface)
        self.focusCard.setObjectName(u"focusCard")
        sizePolicy.setHeightForWidth(self.focusCard.sizePolicy().hasHeightForWidth())
        self.focusCard.setSizePolicy(sizePolicy)
        self.focusCard.setMinimumSize(QSize(380, 410))
        self.focusCard.setMaximumSize(QSize(600, 410))
        self.focusCard.setStyleSheet(u"")
        self.gridLayout_4 = QGridLayout(self.focusCard)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, -1, -1, -1)
        self.focusCardIcon = IconWidget(self.focusCard)
        self.focusCardIcon.setObjectName(u"focusCardIcon")
        self.focusCardIcon.setMinimumSize(QSize(20, 20))
        self.focusCardIcon.setMaximumSize(QSize(20, 20))
        icon1 = QIcon()
        icon1.addFile(u":/images/alarms.png", QSize(), QIcon.Normal, QIcon.Off)
        self.focusCardIcon.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.focusCardIcon)

        self.focusPeriodLabel = StrongBodyLabel(self.focusCard)
        self.focusPeriodLabel.setObjectName(u"focusPeriodLabel")

        self.horizontalLayout_2.addWidget(self.focusPeriodLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pinButton = TransparentToolButton(self.focusCard)
        self.pinButton.setObjectName(u"pinButton")

        self.horizontalLayout_2.addWidget(self.pinButton)

        self.moreButton = TransparentToolButton(self.focusCard)
        self.moreButton.setObjectName(u"moreButton")

        self.horizontalLayout_2.addWidget(self.moreButton)


        self.gridLayout_4.addLayout(self.horizontalLayout_2, 1, 0, 1, 3)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalSpacer_27 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_27)

        self.file_LineEdit = LineEdit(self.focusCard)
        self.file_LineEdit.setObjectName(u"file_LineEdit")
        self.file_LineEdit.setMinimumSize(QSize(276, 33))
        self.file_LineEdit.setMaximumSize(QSize(1920, 33))

        self.horizontalLayout_16.addWidget(self.file_LineEdit)

        self.open_fileButton = HyperlinkButton(self.focusCard)
        self.open_fileButton.setObjectName(u"open_fileButton")

        self.horizontalLayout_16.addWidget(self.open_fileButton)

        self.horizontalSpacer_28 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_28)


        self.gridLayout_4.addLayout(self.horizontalLayout_16, 6, 0, 1, 3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 5, 1, 1, 1)

        self.startFocusButton = PrimaryPushButton(self.focusCard)
        self.startFocusButton.setObjectName(u"startFocusButton")
        self.startFocusButton.setAutoDefault(True)

        self.gridLayout_4.addWidget(self.startFocusButton, 12, 1, 1, 1)

        self.horizontalSpacer_26 = QSpacerItem(101, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_26, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_24 = QSpacerItem(64, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_24)

        self.BodyLabel = BodyLabel(self.focusCard)
        self.BodyLabel.setObjectName(u"BodyLabel")

        self.horizontalLayout.addWidget(self.BodyLabel)

        self.translate_SwitchButton = SwitchButton(self.focusCard)
        self.translate_SwitchButton.setObjectName(u"translate_SwitchButton")

        self.horizontalLayout.addWidget(self.translate_SwitchButton)

        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_21)

        self.country_selector = ComboBox(self.focusCard)
        self.country_selector.setObjectName(u"country_selector")
        self.country_selector.setMinimumSize(QSize(150, 33))

        self.horizontalLayout.addWidget(self.country_selector)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.gridLayout_4.addLayout(self.horizontalLayout, 8, 0, 1, 3)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_11, 12, 2, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 7, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 9, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(15, 10, 15, -1)
        self.horizontalSpacer_20 = QSpacerItem(60, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_20)

        self.hintLabel = BodyLabel(self.focusCard)
        self.hintLabel.setObjectName(u"hintLabel")
        self.hintLabel.setAlignment(Qt.AlignCenter)
        self.hintLabel.setWordWrap(True)
        self.hintLabel.setMargin(0)
        self.hintLabel.setProperty("lightColor", QColor(96, 96, 96))
        self.hintLabel.setProperty("darkColor", QColor(206, 206, 206))

        self.horizontalLayout_6.addWidget(self.hintLabel)

        self.horizontalSpacer_19 = QSpacerItem(23, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_19)


        self.gridLayout_4.addLayout(self.horizontalLayout_6, 4, 0, 1, 3)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_12, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 13, 1, 1, 1)

        self.prepareFocusLabel = SubtitleLabel(self.focusCard)
        self.prepareFocusLabel.setObjectName(u"prepareFocusLabel")
        self.prepareFocusLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.prepareFocusLabel, 3, 1, 1, 1)

        self.horizontalSpacer_25 = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_25, 3, 2, 1, 1)

        self.loading_bar1 = IndeterminateProgressBar(self.focusCard)
        self.loading_bar1.setObjectName(u"loading_bar1")

        self.gridLayout_4.addWidget(self.loading_bar1, 0, 0, 1, 3)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_12, 12, 0, 1, 1)

        self.default_path_checker = CheckBox(self.focusCard)
        self.default_path_checker.setObjectName(u"default_path_checker")
        self.default_path_checker.setLayoutDirection(Qt.RightToLeft)

        self.gridLayout_4.addWidget(self.default_path_checker, 11, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_4, 11, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_5, 11, 0, 1, 1)


        self.gridLayout.addWidget(self.focusCard, 1, 0, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 1, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)

        self.horizontalLayout_3.addLayout(self.gridLayout)


        self.retranslateUi(FocusInterface)

        QMetaObject.connectSlotsByName(FocusInterface)
    # setupUi

    def retranslateUi(self, FocusInterface):
        FocusInterface.setWindowTitle(QCoreApplication.translate("FocusInterface", u"Form", None))
        self.dailyProgressLabel.setText(QCoreApplication.translate("FocusInterface", u"\u5de5\u5177\u7bb1", None))
        self.focusPeriodLabel.setText(QCoreApplication.translate("FocusInterface", u"fluent transfer", None))
        self.file_LineEdit.setText("")
        self.open_fileButton.setText(QCoreApplication.translate("FocusInterface", u"\u6253\u5f00\u6587\u4ef6", None))
        self.startFocusButton.setText(QCoreApplication.translate("FocusInterface", u"\u542f\u52a8\uff01", None))
        self.BodyLabel.setText(QCoreApplication.translate("FocusInterface", u"\u8df3\u8fc7\u7ffb\u8bd1", None))
        self.translate_SwitchButton.setText("")
        self.translate_SwitchButton.setOnText("")
        self.translate_SwitchButton.setOffText("")
        self.hintLabel.setText(QCoreApplication.translate("FocusInterface", u"\u9009\u62e9\u4f60\u8981\u8f6c\u6362\u7684\u97f3\u9891\u6216\u89c6\u9891\uff0c\u7136\u540e\u9009\u62e9\u9700\u8981\u7684\u8bed\u8a00", None))
        self.prepareFocusLabel.setText(QCoreApplication.translate("FocusInterface", u"\u4e00\u952e\u8f6c\u6362\u97f3\u89c6\u9891", None))
        self.default_path_checker.setText(QCoreApplication.translate("FocusInterface", u"\u4fdd\u5b58\u5230\u9ed8\u8ba4\u6587\u4ef6\u5939", None))
    # retranslateUi

