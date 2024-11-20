import items

import unittest

class TestApp(unittest.TestCase):
    def test_get_item(self):
        dummy_id = 'test'
        result = items.get_item(dummy_id)
        self.assertEqual(result, dummy_id)

if __name__ == '__main__':
    unittest.main()
