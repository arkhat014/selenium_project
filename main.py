import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import FirefoxOptions
import time

def get_driver():
    options = {
    'proxy': {
        'http': 'http://mwg1.tsb.kz:3128',
        'https': 'http://mwg1.tsb.kz:3128',
        'no_proxy': 'localhost,127.0.0.1'
    },
    'request_storage': 'memory',
    'request_storage_max_size': 1}
    download_dir = "/root/airflow/dags/Alit/stat_gov"
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    opts.add_argument('--disable-gpu')
    opts.set_preference("browser.download.folderList", 2)
    opts.set_preference('browser.download.manager.showWhenStarting', False)
    opts.set_preference("browser.download.dir", download_dir)
    opts.set_preference('browser.download.useDownloadDir', True)
    opts.set_preference("browser.helperApps.neverAsk.saveToDisk","application/zip")
    driver = webdriver.Firefox(service=Service("/opt/geckodriver"), options=opts, seleniumwire_options=options)
    return driver

def get_application():
    with open('application.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            application = row[5]
            return application

def check_application2(application):
    driver = get_driver()
    driver.get('https://stat.gov.kz/ru/juridical/by/status/')
    driver.find_element(By.XPATH,'/html/body/div[4]/div/div/div[2]/div/div[3]/div/div/input').send_keys(application)
    driver.execute_script("window.scrollBy(0, 100);")
    driver.find_element(By.XPATH,'//*[@id="status"]/div[3]/div/button').click()
    try:
        time.sleep(5)
        driver.find_element(By.LINK_TEXT, 'Скачать').click()
        return True
    except:
        return False