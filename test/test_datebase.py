from database.data_pro import FileManager
import os

# 数据库连接参数
db_params = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123456',
    'database': 'fluent_transfer1',
    'charset': 'utf8mb4'
}


# 创建FileManager实例
file_manager = FileManager(db_params)

# 指定表名
table_name = "file_records"

# 调用add_entry函数增加条目
# 替换以下参数为实际的文件名，语言和文件路径
file_manager.add_entry(table_name, "example233.txt", "English", r"C:\Users\infin\Desktop\123.txt")

# 调用open_file_path函数打开文件路径
# 替换以下参数中的id为你想要打开的文件记录的id
#file_manager.open_file_path(table_name, 3)

# 调用delete_file函数删除文件
# 替换以下参数中的id为你想要删除的文件记录的id
#file_manager.delete_file(table_name, 2)

# 关闭数据库连接
file_manager.close()
