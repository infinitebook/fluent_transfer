import pymysql
import os
import subprocess


# 数据库连接参数
db_params = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123456',
    'database': 'fluent_transfer1',
    'charset': 'utf8mb4'
}


class FileManager:
    def __init__(self, db_params):
        self.conn = pymysql.connect(**db_params)
        self.cursor = self.conn.cursor()

    def add_entry(self, table, file_name, language, file_path):
        """往特定表内增加条目"""
        sql = f"INSERT INTO {table} (file_name, language, file_path) VALUES (%s, %s, %s)"
        try:
            self.cursor.execute(sql, (file_name, language, file_path))
            self.conn.commit()
            print("Entry added successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

    def open_file(self, table, id):
        """通过ID打开对应的文件路径"""
        sql = f"SELECT file_path FROM {table} WHERE id = %s"
        try:
            self.cursor.execute(sql, (id,))
            result = self.cursor.fetchone()
            if result:
                file_path = result[0]
                # 使用Windows文件管理器打开路径
                os.startfile(file_path)
            else:
                print("No entry found with the given ID.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def open_file_path(self, table, id):
        """通过ID打开对应的文件路径"""
        sql = f"SELECT file_path FROM {table} WHERE id = %s"
        try:
            self.cursor.execute(sql, (id,))
            result = self.cursor.fetchone()
            if result:
                file_path = result[0]
                path = os.path.dirname(file_path)
                # 使用Windows文件管理器打开路径
                os.startfile(path)
            else:
                print("No entry found with the given ID.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_file(self, table, id):
        """通过ID删除对应的文件，然后删除数据库中的条目"""
        # 首先获取文件路径
        sql_select = f"SELECT file_path FROM {table} WHERE id = %s"
        auto_increment = "ALTER TABLE file_records AUTO_INCREMENT = 1"
        try:
            self.cursor.execute(sql_select, (id,))
            result = self.cursor.fetchone()
            if result:
                file_path = result[0]
                try:
                    # 尝试删除文件
                    os.remove(file_path)
                    print("File deleted successfully.")
                    # 文件删除成功后，删除数据库中的条目
                    sql_delete = f"DELETE FROM {table} WHERE id = %s"
                    self.cursor.execute(sql_delete, (id,))
                    self.cursor.execute(auto_increment)
                    self.conn.commit()

                    print("Database entry deleted successfully.")


                except Exception as e:
                    print(f"An error occurred when deleting the file: {e}")
                    self.conn.rollback()
            else:
                print("No entry found with the given ID.")
        except Exception as e:
            print(f"An error occurred when selecting the file path: {e}")

    def update_file_path(self, table, old_file_path, new_file_path):
        """更新具有特定file_path的所有条目，将它们的file_path改为新的file_path"""
        sql = f"UPDATE {table} SET file_path = %s WHERE file_path = %s"
        try:
            self.cursor.execute(sql, (new_file_path, old_file_path))
            count = self.cursor.rowcount  # 获取受影响的行数
            self.conn.commit()
            print(f"File path updated successfully in {count} records.")
        except Exception as e:
            print(f"An error occurred while updating the file paths: {e}")
            self.conn.rollback()

    def close(self):
        """关闭数据库连接"""
        self.cursor.close()
        self.conn.close()

# 使用示例
# file_manager = FileManager(db_params)
# file_manager.add_entry('your_table_name', 'example.txt', 'English', 'C:\\path\\to\\your\\file')
# file_manager.open_file_path('your_table_name', 1)
# file_manager.delete_file('your_table_name', 1)
# file_manager.close()
