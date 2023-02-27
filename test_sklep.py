"""
WSB zaliczenie Selenium - PP61398
# Skrypt automatyzujcy przypadki testowe dla: https://automationpractice.pl/
"""
import time
import unittest
import inspect
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class TestyNaZaliczenie(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://automationpractice.pl/")
        self.driver.implicitly_wait(2)

    def tearDown(self):
        self.driver.quit()

    def test_wprowadzona_poprawna_nazwa_artykulu_w_polu_search(self):
        print("ID:001 - klasa: " + self.__class__.__name__ + " -> " + inspect.stack()[0][3])
        search_string = random.choice(["Dress", "T-Shirt", "Blouse"])     # Losowo wybiera nazwe istniejacego produktu
        search_query = self.driver.find_element(By.ID, "search_query_top")
        search_query.click()
        search_query.clear()
        search_query.send_keys(search_string)
        self.driver.find_element(By.NAME, "submit_search").click()
        time.sleep(1)
        results = self.driver.find_elements(By.XPATH, '//ul[@class="product_list grid row"]//a[@class="product-name"]')

        # Sprawdza czy wyswietlil wyniki wyszukiwania
        self.assertGreater(len(results), 0)

        # Sprawdza czy wyniki wyszukiwania sa prawidlowe
        for result in results:
            self.assertIn(search_string.lower(), result.text.lower(), "Nazwa produktu nie zawiera szukanego slowa.")

    def test_poprawnosc_kwoty_po_rabacie(self):
        print("ID:002 - klasa: " + self.__class__.__name__ + " -> " + inspect.stack()[0][3])
        self.driver.find_element(By.CLASS_NAME, "blockbestsellers").click()
        time.sleep(2)
        # Wyszukuje produkty w promocji
        #percent_reduction_node = '//*[@id="homefeatured"]//div[@class="right-block"]//span[@class="price-percent-reduction"]' - juz nie dziala
        percent_reduction_node = '//div[@class="product-container"]//div[@class="right-block"]//span[@class="price-percent-reduction"]'
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

        # Wybiera jeden z promocyjnych produktow i na podstawie starej ceny i podanego % obnizki oblicza nowa cene
        nr_art = random.randint(0, len(percent_reductions)-1)
        old_price = float(old_products_prices[nr_art].text[1:])
        percent = float(percent_reductions[nr_art].text[1:-1]) / 100
        calculated_price = old_price - (old_price * percent)

        # Odczytuje ze strony cene po obnizce i porownuje z ta obliczona podczas testu
        current_price = float(current_products_prices[nr_art].text[1:])
        self.assertAlmostEqual(calculated_price, current_price, 2 , "Niepoprawna cena lub procent obnizki ceny.")

    def test_poprawnosc_kwoty_zakupu(self):
        print("ID:003 - klasa: " + self.__class__.__name__ + " -> " + inspect.stack()[0][3])
        self.driver.find_element(By.CLASS_NAME, "blockbestsellers").click()
        time.sleep(2)
        # Wybiera dwa lub wiecej produktow z wszystkich wyswietlonych na stronie
        all_products = self.driver.find_elements(By.XPATH, '//div[@class="product-container"]')
        product_count = len(all_products)
        self.assertGreater(product_count, 0, "Brak produkow.")
        selected_products = random.sample(range(product_count), random.randint(2, product_count))
        total_price = float(0)  # Cakowita wartosc transakcji
        action = ActionChains(self.driver)

        # Dla kazdego z wybranych produktow otwiera strone szczegolowa i zwieksza liczbe zamawianych sztuk
        for p in selected_products:
            action.move_to_element(all_products[p]).perform()
            more_button_xpath = f'(//div[@class="product-container"])[{p+1}]//a[@title="View"]'
            self.driver.find_element(By.XPATH, more_button_xpath).click()
            # Przechodzi do strony produktu
            price_label = self.driver.find_element(By.ID, 'our_price_display')
            price = float(price_label.text[1:])
            quantity = random.randint(2, 5)  # Zamow w granicach: 2-5 szt.
            total_price = total_price + (price * quantity)
            # Zwieksza przyciskiem "+" liczbe zamawianych sztuk
            for i in range(quantity - 1):
                self.driver.find_element(By.XPATH,
                                         '//a[@class="btn btn-default button-plus product_quantity_up"]').click()
            self.driver.find_element(By.NAME, "Submit").click()
            # Jezeli nie byl to ostatni z wybranych produktow to wraca na glowna strone i kontynuuje zamawianie
            if p != selected_products[-1]:
                self.driver.find_element(By.XPATH, '//span[@title="Continue shopping"]').click()
                self.driver.back()

        # Porzechodzi na strone podsumowania
        self.driver.find_element(By.XPATH, '//a[@title="Proceed to checkout"]').click()
        total_products = self.driver.find_element(By.ID, "total_product")
        total_web_price = float(total_products.text[1:])

        self.assertAlmostEqual(total_web_price, total_price, 2, "Niepoprawna cena bez podatku.")


if __name__ == '__main__':
    unittest.main()
