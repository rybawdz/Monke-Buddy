from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

jokes = open('jokes.txt', 'w', encoding='Utf-8')

driver = webdriver.Firefox()
driver.get('https://edition.cnn.com/interactive/2019/06/us/dad-joke-generator-trnd/')

joke_button = driver.find_element(By.CLASS_NAME, 'push-button')
joke_button.click()

for i in range(100):
    joke_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'joke-text')))
    jokes.write(joke_box.text + '\n')
    next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'show-me-another')))
    next_button.click()

jokes.close()