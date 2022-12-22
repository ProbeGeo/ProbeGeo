import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


class Pictimo_Crawler:
    def __init__(self):
        self.base_url = 'https://www.pictimo.com/'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        })
        self.ipv4_re = r"((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)"
        self.city_re = "^https://www.pictimo.com/" + ".*/" + "(.*)/" + ".*$"
        self.ip_geo = []
        self.error_urls = []
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
        self.driver.implicitly_wait(10)

    def __del__(self):
        self.driver.close()

    def get_countries(self):
        response = self.session.get(urljoin(self.base_url, 'country'))
        soup = BeautifulSoup(response.text, 'lxml')
        countries = [urljoin(self.base_url, item["href"]) for item in soup.find_all('a') if re.match("^country/.*$", item["href"]) is not None]
        return countries

    def get_cameras_of_country(self, url):
        self.driver.get(url)
        js = 'return document.body.scrollHeight;'
        height = 0
        num = 0
        idx = 0
        while True:
            new_height = self.driver.execute_script(js)
            if new_height > height:
                num = 0
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                height = new_height
                print("scrolling", idx)
                idx += 1
                time.sleep(1)
            else:
                num += 1
                height = new_height
                if num >= 3:
                    print("scroll to bottom")
                    break
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        cameras = [urljoin(url, item["href"]) for item in soup.find_all('a', id=True) if re.match("^caml_text_.*$", item["id"]) is not None]
        return cameras

    def get_ip_geo_of_camera(self, url):
        try:
            response = self.session.get(url, timeout=10)
        except:
            print("error: ", url)
            self.error_urls.append(url)
            return None, None, None, None, None
        with open(os.path.join("pictimo_htmls", "+".join(urlparse(url).path.split('/')[1:]) + ".txt"), "w") as f:
            f.write(response.text)
        soup = BeautifulSoup(response.text, 'lxml')
        ip, country, city, latitude, longitude = None, None, None, None, None
        ip_tag = soup.find('img', id='camImage')
        if ip_tag is not None:
            try:
                ip = re.search(self.ipv4_re, soup.find('img', id='camImage')['src']).group(0)
            except:
                print("error: ", url)
                self.error_urls.append(url)
        country, city = url.split('/')[3], url.split('/')[4]
        location_tag = soup.find('div', id='map-canvas')
        if location_tag is not None:
            latitude = location_tag['data-latitude']
            longitude = location_tag['data-longitude']
        return ip, country, city, latitude, longitude

    def run(self):
        countries = self.get_countries()
        print("get countries: ", len(countries))
        num = 0
        for country in countries:
            cameras = self.get_cameras_of_country(country)
            print("get", len(cameras), "cameras in", country.split('/')[4])
            for camera in cameras:
                ip, country, city, latitude, longitude = self.get_ip_geo_of_camera(camera)
                if ip != None and country != None and city != None and latitude != None and longitude != None:
                    self.ip_geo.append([ip, country, city, latitude, longitude])
            num += 1
            print("finished", num, "countries", "remain", len(countries) - num)
        with open("pictimo_results.csv", "w") as f:
            f.write("ip,country,city,latitude,longitude\n")
            for item in self.ip_geo:
                f.write(",".join(item) + "\n")
        with open("pictimo_error_urls.txt", "w") as f:
            f.write("\n".join(self.error_urls))

    def test(self):
        country = self.get_countries()[0]
        camera = self.get_cameras_of_country(country)[0]
        print(self.get_ip_geo_of_camera(camera))

if __name__ == '__main__':
    crawler = Pictimo_Crawler()
    crawler.run()