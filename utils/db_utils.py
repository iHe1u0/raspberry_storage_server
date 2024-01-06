import logging
import os
import sqlite3

from utils.token_utils import encode


class DBUtils:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '..'))
        data_dir = os.path.join(project_root, 'data')  # 数据目录路径
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        db_file = os.path.join(data_dir, 'data.db')
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        logging.basicConfig(level=logging.DEBUG)
        # Create user table
        self.__create_user_table__()

    def check_if_table_exists(self, table_name):
        self.cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?''', (table_name,))
        exists = self.cursor.fetchone()[0]
        return exists > 0

    def check_if_value_exists(self, table_name, key, value):
        """
        Checks if the value exists in the table_name
        :param table_name: db table name
        :param key: db column name
        :param value: db value to check
        :return: id if exists, otherwise None
        """
        query = f'''SELECT id FROM {table_name} WHERE {key} = ? LIMIT 1'''
        self.cursor.execute(query, (value,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # 返回找到的第一行的 ID
        else:
            return None  # 如果没找到符合条件的行，返回 None

    def create_table(self, table_name, columns):
        if self.check_if_table_exists(table_name):
            logging.debug(f'Table {table_name} already exists.')
        else:
            columns_str = ', '.join(columns)
            create_table_query = f'''CREATE TABLE {table_name} ({columns_str})'''
            self.cursor.execute(create_table_query)
            self.conn.commit()
            logging.debug(f'Table {table_name} has been created.')

    def register_user(self, username, password):
        status = 0
        if self.check_if_table_exists('user'):
            if not self.check_if_value_exists('user', 'name', encode(username)):
                try:
                    self.cursor.execute('''INSERT INTO user (name, password, active) VALUES (?, ?, ?)''',
                                        (encode(username), encode(password), True))
                    self.conn.commit()
                    logging.info(f'User {username} has been registered.')
                except sqlite3.Error as e:
                    logging.error(f'Error registering user {username}: {str(e)}')
                    status = -1
            else:
                logging.info(f'user {username} has been registered.')
                status = 1
        else:
            self.__create_user_table__()
            status = -2
        return status

    def login_user(self, username, password):
        if self.check_if_table_exists('user'):
            name_id = int(self.check_if_value_exists('user', 'name', encode(username)))
            if name_id is not None:
                password_id = int(self.check_if_value_exists('user', 'password', encode(password)))
                if name_id == password_id:
                    return True
        else:
            return False

    def __create_user_table__(self):
        name = 'user'
        column = ['id INTEGER PRIMARY KEY', 'name TEXT', 'password TEXT', 'active BOOLEAN']
        self.create_table(name, column)
