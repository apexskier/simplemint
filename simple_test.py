__author__ = 'cameronlittle'

import datetime
import unittest
from simple import SimpleAccess

from private import username, password


class SimpleTest(unittest.TestCase):
    # @unittest.skip('test')
    def test_simple_login(self):
        sa = SimpleAccess(username, password)

    def test_simple_add_goal(self):
        sa = SimpleAccess(username, password)
        f = datetime.datetime(2016, 1, 2)
        sa.new_goal('test goal', 200, f)


if __name__ == '__main__':
    unittest.main()
