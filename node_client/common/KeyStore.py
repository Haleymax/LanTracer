import sqlite3
from typing import Optional

class KeyStore:
    # SQL 查询语句
    CREATE_TABLE_QUERY = '''
    CREATE TABLE IF NOT EXISTS keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key_name TEXT UNIQUE NOT NULL,
        key_value TEXT NOT NULL
    )
    '''

    INSERT_OR_REPLACE_KEY_QUERY = '''
    INSERT OR REPLACE INTO keys (key_name, key_value) VALUES (?, ?)
    '''

    GET_KEY_QUERY = '''
    SELECT key_value FROM keys WHERE key_name = ?
    '''

    UPDATE_KEY_QUERY = '''
    UPDATE keys SET key_value = ? WHERE key_name = ?
    '''

    DELETE_KEY_QUERY = '''
    DELETE FROM keys WHERE key_name = ?
    '''

    def __init__(self, database_path: str = './data/keystore.db'):
        """
        初始化存储数据类
        :param database_path: SQLite 数据库文件名（默认为 keystore.db）
        """
        self.database_path = database_path
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """
        如果表不存在，则创建表
        """
        self.cursor.execute(self.CREATE_TABLE_QUERY)
        self.conn.commit()

    def insert_key(self, key_name: str, key_value: str):
        """
        插入或替换密钥
        :param key_name: 密钥名称
        :param key_value: 密钥值
        """
        self.cursor.execute(self.INSERT_OR_REPLACE_KEY_QUERY, (key_name, key_value))
        self.conn.commit()

    def get_key(self, key_name: str) -> Optional[str]:
        """
        获取密钥值
        :param key_name: 密钥名称
        :return: 密钥值（如果不存在则返回 None）
        """
        self.cursor.execute(self.GET_KEY_QUERY, (key_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_key(self, key_name: str, new_key_value: str):
        """
        更新密钥值
        :param key_name: 密钥名称
        :param new_key_value: 新的密钥值
        """
        self.cursor.execute(self.UPDATE_KEY_QUERY, (new_key_value, key_name))
        self.conn.commit()

    def delete_key(self, key_name: str):
        """
        删除密钥
        :param key_name: 密钥名称
        """
        self.cursor.execute(self.DELETE_KEY_QUERY, (key_name,))
        self.conn.commit()

    def close(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        """
        支持上下文管理器（with 语句）
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        支持上下文管理器（with 语句）
        """
        self.close()

if __name__ == '__main__':
    with KeyStore() as store:
        # 插入或替换密钥
        store.insert_key('api_key', '12345-ABCDE-67890')
        store.insert_key('secret_key', '98765-ZYXWV-43210')

        # 获取密钥
        api_key = store.get_key('secret')
        print("API Key:", api_key)  # 输出：API Key: 12345-ABCDE-67890

        # 更新密钥
        store.update_key('api_key', 'NEW-API-KEY-12345')
        updated_api_key = store.get_key('api_key')
        print("Updated API Key:", updated_api_key)  # 输出：Updated API Key: NEW-API-KEY-12345

        # 删除密钥
        store.delete_key('secret_key')
        deleted_key = store.get_key('secret_key')
        print("Deleted Secret Key:", deleted_key)
