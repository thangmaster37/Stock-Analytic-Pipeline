import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://banggia.hnx.vn")

# time.sleep(4)

# search_field = driver.find_element(By.NAME, 'q')

# search_field.send_keys('bobbyhadz.com')

# search_field.submit()

time.sleep(2)

driver.close()
