from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os

class Browser():
    driver = None
    quited = False

    def __del__(self):
        self.quit()

    def __init__(self):

        HUB_URL = self.get_hub_url()

        options = webdriver.ChromeOptions()        
        options.add_experimental_option("prefs", {
            "download.default_directory": "/app_data/"
        })

        self.driver = webdriver.Remote(
            command_executor=HUB_URL,
            options=options
        )

    def get_hub_url(self) -> str:
        HUB_URL = os.environ.get('CN_SE_HUB')
        HUB_PORT = os.environ.get('SE_WEB_PORT')
        return "http://%s:%s/wd/hub" % (HUB_URL, HUB_PORT)

    def init_url(self, url:str):
        self.driver.implicitly_wait(30)
        self.driver.get(url)

            # assert "Python" in self.driver.title
            # elem = self.driver.find_element(By.NAME, "q")
            # elem.send_keys("documentation")
            # elem.send_keys(Keys.RETURN)
            # assert "No results found." not in self.driver.page_source
            # 
            
    def print(self):
        print(self.driver.page_source)

    def quit(self):
        if self.quited == False:
            self.quited = True
            self.driver.quit()

    def get_elems(self, selector):
        return self.driver.find_element_by_css_selector(selector)