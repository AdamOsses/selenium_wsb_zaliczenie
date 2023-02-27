# Projekt zaliczeniowy WSB:  Automatyzacja przypadków testowych przy pomocy Selenium Webdriver #  

---  

---
## Środowisko: ##  

---  
### 1. Virtualenv: ###
```commandline
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```
### 2. Sterownik Google Chrome: <https://chromedriver.storage.googleapis.com/index.html?path=106.0.5249.61/> ###  
```net  
wget -N https://chromedriver.storage.googleapis.com/106.0.5249.61/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
rm ~/chromedriver_linux64.zip
chmod +x chromedriver
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
```  

## Info: ##  

---  
Testowana strona internetowa: https://automationpractice.pl/  
Przeglądarka: Google Chrome

## II 2023 ##  
Strona ulegla zmianom - poprawione lokalizatory.