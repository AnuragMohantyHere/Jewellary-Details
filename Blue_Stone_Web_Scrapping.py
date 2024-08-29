from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["BlueStone"]
collection = db["jewellary"]
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

webdriver_service = Service("C:\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
driver.get("https://www.bluestone.com/jewellery.html")
try:
    count=1
    c=1
    while c <=11:
        details={'SL.NO':'','Name':'','Price':'','Product_URL':'','Image_URL':'','Category':''}
        driver.execute_script("window.scrollBy(0, 500);")
        wait = WebDriverWait(driver, 120)
        wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="product_list_ui"]/li[{count}]')))
        elements = driver.find_elements(By.XPATH, f'//*[@id="product_list_ui"]/li[{count}]')
        for e in elements:
            x = e.find_element(By.XPATH, f'//*[@id="product_list_ui"]/li[{count}]').text
            if 'RS' not in x:
                count+=1
                continue
            details['Name'] = x.split('\n')[0]
            Both_Price = x.split('\n')[1]
            details['Price'] = Both_Price.split(' ')[0]
            details['Product_URL'] = e.find_element(By.XPATH, f'//*[@id="product_list_ui"]/li[{count}]').get_attribute('data-url')
            details['Image_URL'] = e.find_element(By.TAG_NAME, 'img').get_attribute('src')
            product_driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
            product_driver.get(details['Product_URL'])
            wait = WebDriverWait(product_driver, 120)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="breadcrumb"]/ul/li[3]/a/span')))
            details['Category'] = product_driver.find_element(By.XPATH, '//*[@id="breadcrumb"]/ul/li[3]/a/span').text
            details['SL.NO']=str(c)
            print(details)
            count+=1
            c+=1
            result = collection.insert_one(details)

finally:
    driver.quit()
