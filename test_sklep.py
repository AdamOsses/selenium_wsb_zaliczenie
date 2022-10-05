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
        print("ID:001 - klasa: " + self.__class__.__name__ + " -> " + inspect.stack()[0][3])
        visible_buttons = self.driver.find_elements\
            (By.XPATH, '//ul[@class="sf-menu clearfix menu-content sf-js-enabled sf-arrows"]/li')
        self.assertGreater(len(visible_buttons), 0)

        target_button = visible_buttons[random.randint(0, len(visible_buttons)-1)] # Losowo wybiera przycisk
        target_button.click()
        results = self.podaj_wyfiltrowane_produkty()
        self.assertGreater(len(results), 0, "Strona nie wyswietlila zadnego produktu.")

    def test_wprowadzona_poprawna_nazwa_artykulu(self):
        print("ID:002 - klasa: " + self.__class__.__name__ + " -> " + inspect.stack()[0][3])
        search_string = random.choice(["Dress", "T-Shirt", "Blouse"])     # Losowo wybiera nazwe istniejacego produktu
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
            # print(result.text, end=', ')
            self.assertIn(search_string.lower(), result.text.lower(), "Nazwa produktu nie zawiera szukanego slowa.")

    def test_poprawnosc_kwoty_po_rabacie(self):
        print("ID:003 - klasa: " + self.__class__.__name__ + " -> " + inspect.stack()[0][3])
        # Wyszukuje produkty w promocji
        percent_reduction_node = '//*[@id="homefeatured"]//div[@class="right-block"]//span[@class="price-percent-reduction"]'
        percent_reductions = self.driver.find_elements(By.XPATH, percent_reduction_node)
        old_products_prices = self.driver.find_elements(By.XPATH,\
                            percent_reduction_node + '//preceding-sibling::span[@class="old-price product-price"]')
        current_products_prices = self.driver.find_elements(By.XPATH,\
                            percent_reduction_node + '//preceding-sibling::span[@class="price product-price"]')

        # Sprawdza czy jest tyle samo wezlow old_product_prices, current_products_prices i old_products_prices
        self.assertEqual(len(percent_reductions), len(old_products_prices), 'Nierowna liczba wezlow.')
        self.assertEqual(len(percent_reductions), len(current_products_prices), 'Nierowna liczba wezlow.')

        if len(percent_reductions) == 0:
            self.skipTest("Na stronie brak produktow w promocji.")

        # Wybiera jeden z promocyjnych produktow i na podstawie starej ceny i podanego % obnizki oblicza nowa cene.
        art = random.randint(0, len(percent_reductions)-1)
        old_price = float(old_products_prices[art].text[1:])
        current_price = float(current_products_prices[art].text[1:])
        percent = float(percent_reductions[art].text[1:-1]) / 100
        calculated_price = old_price - (old_price * percent)

        self.assertAlmostEqual(calculated_price, current_price, 2 , "Niepoprawna cena lub procent obnizki ceny.")


if __name__ == '__main__':
    unittest.main()
