import unittest

from utils.db_utils import DBUtils


class DBTest(unittest.TestCase):

    def test_create_table(self):
        db = DBUtils()
        is_exist = db.check_if_table_exists('user')
        self.assertTrue(is_exist)
        # create user table
        name = 'user'
        column = ['id INTEGER PRIMARY KEY', 'name TEXT', 'password TEXT', 'active BOOLEAN']
        db.create_table(name, column)
        db.register_user('kt', '1109')


if __name__ == '__main__':
    unittest.main()
