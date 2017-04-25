from selenium import webdriver
import unittest


class TestHomepage(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'KhanLine')

if __name__ == "__main__":
    unittest.main()
