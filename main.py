import zipfile
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import glob
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
import csv

url = ""
def check_application(date, type, code):
    driver = webdriver.Firefox()
    driver.get('https://stat.gov.kz/ru/juridical/by/filter/')
    time.sleep(2)
    driver.execute_script("window.scrollBy(0, 100);")
    select = Select(driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[3]/div[1]/div/select'))
    select.select_by_visible_text(date)
    select = Select(driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[3]/div[2]/div/select'))
    select.select_by_visible_text(type)
    select = Select(driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[3]/div[3]/div/select'))
    select.select_by_visible_text(code)
    time.sleep(1)
    driver.find_element(By.ID, '741880_anchor').click()
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, 1200);")
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="filter"]/div[3]/div[9]/button').click()
    try:
        time.sleep(5)
        driver.find_element(By.LINK_TEXT, 'Скачать').click()
        return True
    except:
        return False

def unzip_file(zip_file_path, extract_to_path):
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)
        print(f"Файл {zip_file_path} успешно разархивирован в {extract_to_path}")
        os.remove(zip_file_path)
        print(f"Файл {zip_file_path} удален.")
    except Exception as e:
        print(f"Произошла ошибка при разархивации файла {zip_file_path}: {str(e)}")

def get_latest_zip_filename(directory):
    directory_path = os.path.join(directory, "*.zip")
    list_of_files = glob.glob(directory_path)
    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        zip_filename = os.path.basename(latest_file)
        return zip_filename
    else:
        return None

def get_application_name(date, type, code):
    driver = webdriver.Firefox()
    driver.get('https://stat.gov.kz/ru/juridical/by/filter/')
    time.sleep(3)
    select = Select(driver.find_element(By.XPATH, '//*[@id="filter"]/div[3]/div[1]/div/select'))
    select.select_by_visible_text(date)
    select = Select(driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[3]/div[2]/div/select'))
    select.select_by_visible_text(type)
    select = Select(driver.find_element(By.XPATH, '//*[@id="filter"]/div[3]/div[3]/div/select'))
    select.select_by_visible_text(code)
    driver.find_element(By.ID, '741880_anchor').click()
    time.sleep(5)
    driver.execute_script("window.scrollBy(0, 1400);")
    time.sleep(2)
    element_1 = driver.find_element(By.XPATH, '//*[@id="filter"]/div[3]/div[9]/button')
    driver.find_element(By.XPATH, '//*[@id="filter"]/div[3]/div[9]/button').click()
    time.sleep(4)
    element_1 = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[4]/div[2]/div/div[3]/div[2]/a')
    global url
    url = element_1.get_attribute('href')
    element = driver.find_element(By.CSS_SELECTOR,'div.divTableRow:nth-child(1) > div:nth-child(2)')
    application = element.text
    return application

def check_application2(application):
    driver = webdriver.Firefox()
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

def send_data(application,date,type,code,kato,status,url):
    if status == True:
        status = "Обработан"
    elif status == False:
        status = "Создается"
    data = [
        {"Период": date,"Тип":type,"Ситуационный код":code,"Населенный пункт(КАТО)":kato,"Номер заявки":application,"Статус":status,"Ссылка": url },
]

    text_to_write = application
    csv_file_name = "/Users/arkhatkaiyrzhan/Downloads/application.csv"
    with open(csv_file_name, mode='w', newline='') as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=["Период", "Тип", "Ситуационный код","Населенный пункт(КАТО)","Номер заявки","Статус","Ссылка"])

        writer.writeheader()

        writer.writerows(data)


date = input("Дата :")
type = input("Тип :")
code = input("Код :")
kato = input("Населенный пункт(КАТО) :")
result = check_application(date, type, code)
application = str(get_application_name(date, type, code))
time.sleep(5)
if result == True:
   result_3 = get_latest_zip_filename('/Users/arkhatkaiyrzhan/Downloads/')
   result_2 = unzip_file("/Users/arkhatkaiyrzhan/Downloads/" + result_3, "/Users/arkhatkaiyrzhan/Downloads")
   result_4 = send_data(application,date,type,code,kato,result,url)
   print('Complited')
elif result == False:
   time.sleep(2)
   new_result = check_application2(application)
   if new_result == True:
       result_3 = get_latest_zip_filename('/Users/arkhatkaiyrzhan/Downloads/')
       result_2 = unzip_file("/Users/arkhatkaiyrzhan/Downloads/" + result_3, "/Users/arkhatkaiyrzhan/Downloads")
       result_4 = send_data(application,date,type,code,kato,result,url)
       print('Complited')
   else:
       result_4 = send_data(application,date,type,code,kato,result,url)
       print('Not Complited')
