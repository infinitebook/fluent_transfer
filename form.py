# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QWidget)

from qfluentwidgets import (CheckBox, ComboBox, DotInfoBadge, HyperlinkButton,
    IconInfoBadge, IndeterminateProgressBar, IndeterminateProgressRing, InfoBadge,
    InfoBar, ProgressBar, ProgressRing, PushButton,
    RadioButton, StateToolTip, SwitchButton)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(699, 548)
        self.CheckBox = CheckBox(Form)
        self.CheckBox.setObjectName(u"CheckBox")
        self.CheckBox.setGeometry(QRect(80, 30, 93, 22))
        self.ComboBox = ComboBox(Form)
        self.ComboBox.setObjectName(u"ComboBox")
        self.ComboBox.setGeometry(QRect(90, 70, 77, 32))
        self.HyperlinkButton = HyperlinkButton(Form)
        self.HyperlinkButton.setObjectName(u"HyperlinkButton")
        self.HyperlinkButton.setGeometry(QRect(60, 130, 129, 31))
        self.SwitchButton = SwitchButton(Form)
        self.SwitchButton.setObjectName(u"SwitchButton")
        self.SwitchButton.setGeometry(QRect(50, 190, 76, 22))
        self.RadioButton = RadioButton(Form)
        self.RadioButton.setObjectName(u"RadioButton")
        self.RadioButton.setGeometry(QRect(40, 230, 113, 24))
        self.ProgressRing = ProgressRing(Form)
        self.ProgressRing.setObjectName(u"ProgressRing")
        self.ProgressRing.setGeometry(QRect(50, 340, 100, 100))
        self.ProgressBar = ProgressBar(Form)
        self.ProgressBar.setObjectName(u"ProgressBar")
        self.ProgressBar.setGeometry(QRect(320, 70, 91, 4))
        self.IndeterminateProgressBar = IndeterminateProgressBar(Form)
        self.IndeterminateProgressBar.setObjectName(u"IndeterminateProgressBar")
        self.IndeterminateProgressBar.setGeometry(QRect(320, 100, 91, 4))
        self.IndeterminateProgressRing = IndeterminateProgressRing(Form)
        self.IndeterminateProgressRing.setObjectName(u"IndeterminateProgressRing")
        self.IndeterminateProgressRing.setGeometry(QRect(310, 210, 80, 80))
        self.StateToolTip = StateToolTip(Form)
        self.StateToolTip.setObjectName(u"StateToolTip")
        self.StateToolTip.setGeometry(QRect(310, 380, 256, 51))
        self.InfoBadge = InfoBadge(Form)
        self.InfoBadge.setObjectName(u"InfoBadge")
        self.InfoBadge.setGeometry(QRect(270, 480, 23, 17))
        self.DotInfoBadge = DotInfoBadge(Form)
        self.DotInfoBadge.setObjectName(u"DotInfoBadge")
        self.DotInfoBadge.setGeometry(QRect(350, 490, 4, 4))
        self.IconInfoBadge = IconInfoBadge(Form)
        self.IconInfoBadge.setObjectName(u"IconInfoBadge")
        self.IconInfoBadge.setGeometry(QRect(420, 480, 16, 16))
        self.InfoBar = InfoBar(Form)
        self.InfoBar.setObjectName(u"InfoBar")
        self.InfoBar.setGeometry(QRect(70, 430, 489, 50))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.CheckBox.setText(QCoreApplication.translate("Form", u"Check box", None))
        self.HyperlinkButton.setText(QCoreApplication.translate("Form", u"Hyperlink button", None))
        self.RadioButton.setText(QCoreApplication.translate("Form", u"Radio button", None))
    # retranslateUi

