"""
WSB zaliczenie Selenium - PP61398
# Skrypt automatyzujcy przypadki testowe dla: https://automationpractice.com/
"""

import unittest
import inspect
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


class WyszukiwanieArtykulow(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://automationpractice.com/")

    def tearDown(self):
        self.driver.quit()

    def podaj_wyfiltrowane_produkty(self):
        products = self.driver.find_elements(By.XPATH, '//ul[@class="product_list grid row"]//a[@class="product-name"]')
        return products

    def test_klikniety_przycisk_wyszukiwania_kategorii(self):
        print("ID:001 - uruchamiam klase: " + self.__class__.__name__ + " -> " + inspect.stack()[0][3])
        sleep(5)
        visible_buttons = self.driver.find_elements\
            (By.XPATH, '//ul[@class="sf-menu clearfix menu-content sf-js-enabled sf-arrows"]/li')
        self.assertGreater(len(visible_buttons), 0)
        target_button = visible_buttons[random.randint(0, len(visible_buttons)-1)] # Wybiera przycisk
        target_button.click()
        sleep(1)
        results = self.podaj_wyfiltrowane_produkty()
        self.assertGreater(len(results), 0)

    def test_wprowadzona_poprawna_nazwa_artykulu(self):
        print("ID: 002 - uruchamiam klase: " + self.__class__.__name__ + " -> " + inspect.stack()[0][3])
        search_string = random.choice(["Dress", "T-Shirt", "Blouse"])     # Wybiera nazwe istniejacego produktu
        search_query = self.driver.find_element(By.ID, "search_query_top")
        search_query.click()
        search_query.clear()
        search_query.send_keys(search_string)
        self.driver.find_element(By.NAME, "submit_search").click()
        results = self.podaj_wyfiltrowane_produkty()

        # Sprawdza czy wyswietlil wyniki wyszukiwania:
        self.assertGreater(len(results), 0)

        # Sprawdza czy wyniki wyszukiwania sa prawidlowe:
        for result in results:
            # print(result.text, end='-')
            self.assertIn(search_string.lower(), result.text.lower())
        sleep(1)

        # Dodac: przypadek 003 - wyszukaj produkt w promocji (-x%) i sprawdz prawidlowosc kwoty przeceny


if __name__ == '__main__':
    unittest.main(verbosity=2)
