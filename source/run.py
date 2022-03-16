from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pymysql.cursors
import os

HUB_URL = os.environ.get('CN_SE_HUB')
HUB_PORT = os.environ.get('SE_WEB_PORT')
MYSQL_DB = os.environ.get('MYSQL_DATABASE')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT'))
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')

HUB_URL="http://%s:%s/wd/hub" % (HUB_URL, HUB_PORT)

driver = webdriver.Remote(
    command_executor=HUB_URL,
    options=webdriver.ChromeOptions()
)

try:
    driver.implicitly_wait(30)
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element(By.NAME, "q")
    elem.send_keys("documentation")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    print('this is running on a grid0')
    
finally:
    driver.quit()

connection = pymysql.connect(host=MYSQL_HOST,
                            port=MYSQL_PORT,
                            user=MYSQL_USER,
                            password=MYSQL_PASSWORD,
                            database=MYSQL_DB,
                            cursorclass=pymysql.cursors.DictCursor)

with connection:

    with connection.cursor() as cursor:
        # Read a single record
        sql = "show databases"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)