"""
WSB zaliczenie Selenium - PP 61398
# Skrypt automatyzujcy przypadki testowe dla: https://automationpractice.com/
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class WyszukiwanieArtykulow(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_wprowadzona_poprawna_nazwa_artykulu(self):
        # id="search_query_top"
        pass


if __name__ == '__main__':
    unittest.main()
