# coding:utf-8
import pymysql
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QTreeWidgetItem, QHBoxLayout, QTreeWidgetItemIterator, QTableWidgetItem, \
    QTableWidget
from qfluentwidgets import TreeWidget, TableWidget

from interface.gallery_interface import GalleryInterface, ToolBar
from database.data_pro import FileManager

db_params = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123456',
    'database': 'fluent_transfer1',
    'charset': 'utf8mb4'
}



class ViewInterface(GalleryInterface,FileManager):
    """ View interface """

    def __init__(self, parent=None):
        FileManager.__init__(self, db_params)

        super().__init__(
            title="库",
            subtitle="在此查看您的过往字幕文件",
            parent=parent
        )
        self.setObjectName('viewInterface')
        self.tableFrame = TableFrame(self)
        self.addExampleCard(
            title=self.tr('字幕文件'),
            widget=self.tableFrame,  # 使用引用而不是新的实例
        )
        self.connectThemeButton(self.refresh_table_data)
        self.connectSupportButton(self.openSelectedFilePath)
        self.connectOpenfileButton(self.openSelectedFile)
        self.connectDeleteButton(self.deleteSelectedFile)

    def refresh_table_data(self):
        """处理themeButton点击事件，刷新表格数据"""
        self.tableFrame.load_data_from_db()

    def openSelectedFilePath(self):
        if self.tableFrame.selectedItemId:
            self.open_file_path("file_records", self.tableFrame.selectedItemId)  # 假设表名为file_records
            #FileManager.open_file_path(self,"file_records", 3)
    def openSelectedFile(self):
        if self.tableFrame.selectedItemId:
            self.open_file("file_records", self.tableFrame.selectedItemId)

    def deleteSelectedFile(self):
        if self.tableFrame.selectedItemId:
            self.delete_file("file_records", self.tableFrame.selectedItemId)
            self.tableFrame.load_data_from_db()

class TableFrame(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 初始化表格视图设置
        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)
        self.setColumnCount(5)  # 包括id, 名称, 语言, 文件路径, 创建时间
        self.setHorizontalHeaderLabels([
            self.tr('id'), self.tr('名称'), self.tr('语言'),
            self.tr('文件路径'), self.tr('创建时间')
        ])

        # 从数据库加载数据
        self.load_data_from_db()

        self.setFixedSize(725, 500)
        self.resizeColumnsToContents()

        self.selectedItemId = None  # 用于存储选中行的ID
        self.setSelectionBehavior(QTableWidget.SelectRows)  # 设置为选中整行
        self.itemSelectionChanged.connect(self.onSelectionChanged)  # 连接信号

    def load_data_from_db(self):
        # 连接数据库参数
        db_params = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root123456',
            'database': 'fluent_transfer1',
            'charset': 'utf8mb4'
        }
        # 连接到数据库
        conn = pymysql.connect(**db_params)
        cursor = conn.cursor()
        try:
            # 执行查询
            cursor.execute("SELECT id, file_name, language, file_path, created_at FROM file_records")
            results = cursor.fetchall()
            self.setRowCount(len(results))  # 根据结果设置行数
            for i, row in enumerate(results):
                for j, value in enumerate(row):
                    # 设置单元格数据
                    self.setItem(i, j, QTableWidgetItem(str(value)))
        except pymysql.Error as e:
            print(f"Error: {e}")
        finally:
            # 清理工作
            cursor.close()
            conn.close()

    def onSelectionChanged(self):
        selectedItems = self.selectedItems()
        if selectedItems:
            row = selectedItems[0].row()  # 假设ID位于第一列
            self.selectedItemId = self.item(row, 0).text()

