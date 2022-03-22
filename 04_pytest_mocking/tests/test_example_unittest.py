import unittest
from unittest.mock import patch

from src.example import foo

class MyTestCase(unittest.TestCase):

    # mock where the object is imported into,
    # not where the object is imported from
    # @patch('src.db.db_write')  # WRONG!
    @patch('src.example.db_write')
    def test_foo(self, mock_db_write):
        """
        what happens here is that
        the call to db_write
        is replaced with a call to MagicMock,
        and we have access to this mock
        through mock_db_write param of this function
        """
        mock_db_write.return_value = 10
        x = foo()
        self.assertEqual(x, 10)
