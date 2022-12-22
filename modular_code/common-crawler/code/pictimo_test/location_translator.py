from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
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
        self.driver = webdriver.Chrome(options = option,
                                       chrome_options = chrome_Options)
        self.init_web_page()

    def init_web_page(self):
        url = "https://maplocation.sjfkai.com/"

        print("Location Translator Starting...\n")
        self.driver.get(url)
        print("Location Translator Started!\n")

        googleRadio = self.driver.find_element_by_xpath("//input[@value='google']")
        googleRadio.click()

    def translate_location(self, location):
        textarea = self.driver.find_element_by_id("locations")
        textarea.clear()
        textarea.send_keys(location)

        submit_button = self.driver.find_element_by_xpath('//button[@class="ant-btn ant-btn-primary"]')
        submit_button.click()

        search_result = []
        while (len(search_result) == 0):
            search_result = self.driver.find_elements_by_xpath('//tr[@class="ant-table-row ant-table-row-level-0"]/td')

        if (search_result[9] == "ZERO_RESULTS"):
            print("Location Not Found!")
            return None, None

        longitude = search_result[2].text
        latitude = search_result[3].text
        print("Found coordinate:", longitude, latitude)

        clear_button = self.driver.find_elements_by_xpath('//div[@class="ant-col"]/button[2]')
        clear_button[0].click()

        return longitude, latitude


if __name__ == '__main__':
    location_inquirier = location_translator()
    location_inquirier.translate_location("四川大学望江校区")
    time.sleep(2)
    location_inquirier.translate_location("四川大学江安校区")
