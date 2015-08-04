__author__ = 'cameronlittle'

import datetime
import unittest
from mint import MintAccess, AuthenticationError

from private import mint_username, mint_password


class MintTest(unittest.TestCase):
    def test_mint_failed_login(self):
        self.assertRaises(AuthenticationError, lambda: MintAccess('none', 'none'))

    def test_mint_login(self):
        ma = MintAccess(mint_username, mint_password)
        self.assertIsNotNone(ma)

    """
    def test_mint_categories(self):
        categories = MintAccess(mint_username, mint_password).categories
        self.assertIsNotNone(categories)
    """


if __name__ == '__main__':
    unittest.main()
