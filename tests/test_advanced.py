# -*- coding: utf-8 -*-

from .context import dfvalidate

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(dfvalidate.hmm())


if __name__ == '__main__':
    unittest.main()
