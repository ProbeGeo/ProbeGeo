from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


class location_translator():
    def __init__(self):
        # disable visible interface
        chrome_Options = Options()
        chrome_Options.add_argument('--headless')
        chrome_Options.add_argument('--disable-gpu')
        chrome_Options.add_argument('--no-sandbox')

        # evasion
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome('/root/gww/lmminer/chromedriver', options = option,
                                       chrome_options = chrome_Options)
        self.init_web_page()

    def init_web_page(self):
        url = "https://www.piliang.tech/reverse-geocoding"

        print("Location Translator Starting...\n")
        self.driver.get(url)
        print("Location Translator Started!\n")

    def translate_longitude_latitude(self, longitude, latitude):
        textarea = self.driver.find_element(By.ID, "reverse-form_location")
        textarea.clear()

        clear_button = self.driver.find_element_by_xpath('//button[@class="ant-btn ant-btn-danger"]')
        if clear_button.is_clickable():
            clear_button.click()
        
        textarea.send_keys(latitude + "," + longitude)

        submit_button = self.driver.find_element_by_xpath('//button[@type="submit"]')
        submit_button.click()
        
        search_result = []
        while (len(search_result) == 0):
            search_result = self.driver.find_elements_by_xpath('//tr[@class="ant-table-row ant-table-row-level-0"]/td')

        location, province, city, district, location_distance, poi_name, poi_location, poi_distance = search_result[1].text, search_result[2].text, search_result[3].text, search_result[4].text, search_result[5].text, search_result[6].text, search_result[7].text, search_result[8].text

        return location, province, city, district, location_distance, poi_name, poi_location, poi_distance

    def __del__(self):
        if self.driver:
            self.driver.quit()


if __name__ == '__main__':
    location_inquirier = location_translator()
    location_inquirier.translate_longitude_latitude("116.404,39.915")
