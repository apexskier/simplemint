__author__ = 'cameronlittle'

import datetime
import unittest
from mint import MintAccess

from private import mint_username, mint_password


class MintTest(unittest.TestCase):
    def test_mint_login(self):
        ma = MintAccess(mint_username, mint_password)


if __name__ == '__main__':
    unittest.main()
