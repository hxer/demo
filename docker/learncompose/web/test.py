import unittest

from app import app


class MainTestCase(unittest.TestCase):


    def test_two_and_two(self):
        four = 2 + 2
        self.assertEqual(four, 4)
        self.assertNoEqual(four, 6)

if __name__ == "__main__":
    unittest.main()
