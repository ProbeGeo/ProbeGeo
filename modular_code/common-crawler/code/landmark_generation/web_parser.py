from bs4 import BeautifulSoup
import os
import re
import spacy
import pytesseract as OCR
import cv2
import urllib
from urllib.request import urlopen
import numpy as np
from PIL import Image
from io import BytesIO
import easyocr
from typing import Tuple



class web_parser():
    def __init__(self, url: str, text: str, reader, translator):
        self.url = url
        self.text = text

        self.feature_vector = []
        self.ipv4_count = 0
        self.domain_name_count = 0
        self.candidate_tags = []
        self.parent_children_dic = dict()
        self.title_list = []
        self.meta_list = []
        self.img_list = []
        self.GPE_set = set()
        self.ipv4_set = set()
        self.longitude_set = set()
        self.latitude_set = set()

        self.reader = reader
        self.translator = translator

    def parse(self) -> Tuple[list, list, list]:
        soup = BeautifulSoup(self.text, "lxml")

        self.find_candidate_tags(soup)

        # print(self.ipv4_set)
        # print(self.longitude_set)
        # print(self.latitude_set)

        # if coordination not found, then translate geographic named entity to coordination
        if (len(self.ipv4_set) != 0 and (len(self.longitude_set) == 0 or len(self.latitude_set) == 0)):
            self.extract_info(soup)
            # cannot find geographic named entities
            if(len(self.GPE_set) == 0):
                self.ipv4_set.clear()
                return list(self.ipv4_set), list(self.longitude_set), list(self.latitude_set)

            query_str = str()
            # concatenate location entity
            for item in self.GPE_set:
                query_str += item + ', '

            longitude, latitude = self.translator.translate_location(query_str)
            self.longitude_set.add(longitude)
            self.latitude_set.add(latitude)
        return list(self.ipv4_set), list(self.longitude_set), list(self.latitude_set)

    def translate_coord(self, coordinate):
        coordinate_split = re.split(u"°|\'|\"", coordinate)[:3]
        res = ""
        if len(coordinate_split) == 3:
            x = [float(j) for j in coordinate_split]
            res = x[0] + x[1] / 60 + x[2] / 3600

        return res

    def extract_ipv4(self, d: BeautifulSoup):
        ipv4_re = r"((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)(/([0-2][0-9]|3[0-2]|[0-9]))?"
        result = re.search(ipv4_re, d.decode())
        if (result != None):
            self.ipv4_set.add(result.group())
            self.candidate_tags.append(d)
            parent_tag = d.parent
            if (not parent_tag in self.parent_children_dic.keys()):
                set = {d}
                self.parent_children_dic[parent_tag] = set
                pass
            else:
                self.parent_children_dic[parent_tag].add(d)

    def extract_coodinate(self, d: BeautifulSoup):
        # regular expression to match strings like: Latitude: 142.3245
        longitude_re = r"(longitude)[:,]?\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)"
        latitude_re = r"(latitude)[:,]?\s*[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)"

        # regular expression to match strings like: 72°23'45" E
        lon_degree_re = r'''(((\d|[1-8]\d)[°](\d|[0-5]\d)['](\d|[0-5]\d)(\.\d{1,2})?["]?)|(90[°]0[']0["]?))\s*[EW]'''
        lat_degree_re = r'''(((\d|[1-8]\d)[°](\d|[0-5]\d)['](\d|[0-5]\d)(\.\d{1,2})?["]?)|(90[°]0[']0["]?))\s*[NS]'''

        lon_result = re.search(longitude_re, d.decode(), re.M | re.I)
        lat_result = re.search(latitude_re, d.decode(), re.M | re.I)

        if (lon_result is None):
            lon_deg_result = re.search(lon_degree_re, d.decode(), re.M | re.I)
            if (lon_deg_result is not None):
                lon_deg_result = self.translate_coord(lon_deg_result.group())
                self.longitude_set.add(lon_deg_result)
        else:
            lon_result = re.search(r"[-+]?\d+\.?\d*", lon_result.group())
            self.longitude_set.add(lon_result.group())

        if (lat_result is None):
            lat_deg_result = re.search(lat_degree_re, d.decode(), re.M | re.I)
            if (lat_deg_result is not None):
                lat_deg_result = self.translate_coord(lat_deg_result.group())
                self.latitude_set.add(lat_deg_result)
        else:
            lat_result = re.search(r"[-+]?\d+\.?\d*", lat_result.group())
            self.latitude_set.add(lat_result.group())

    def find_candidate_tags(self, soup: BeautifulSoup):

        domain_name_re = r"https?://[-a-zA-Z0-9._:%\+~#=]{2,256}\.([a-z]{2,6}|\d{1,3})\b([-a-zA-Z0-9._:%\+~#=?&;\(\)\[\]]*)"

        if (soup.descendants == None):
            return
        for d in soup.descendants:
            # check whether d is a leaf node or not
            if (hasattr(d, 'contents')):
                if (len(d.contents) == 0 or (len(d.contents) == 1 and isinstance(d.contents[0], str))):
                    # using regex to extract IPv4
                    self.extract_ipv4(d)

                    # using regex to extract Longitude and latitude
                    self.extract_coodinate(d)

                    # TODO: extract longitude and latitude from google map iframe


                    # TODO: extract infomation from domain name
                    # domain_name_results = re.search(domain_name_re, d.decode(), re.M | re.I)
                    


    def find_geo_entity(self, content: str):
        # nlp = spacy.load("xx_ent_wiki_sm")
        nlp = spacy.load('en_core_web_sm')
        ruler = nlp.add_pipe("entity_ruler")

        # 实体和模式列表
        patterns = [
            {
                # potential location
                "label": "PLOC",
                "pattern": [
                    {"POS": {"IN": ["NOUN", "PROPN"]}},
                    {"IS_PUNCT": True},
                    {"ENT_TYPE": "GPE"}
                ]
            },
            {
                # potential location
                "label": "PLOC",
                "pattern": [
                    {},
                    {"POS": "PROPN"},
                    {"ORTH": ","},
                    {"POS": "PROPN"}
                ]
            },
            {
                # city
                "label": "CITY",
                "pattern": [
                    {"LOWER": "city"},
                    {"IS_PUNCT": True},
                    {"POS": "PROPN"},
                ]
            },
            {
                # country
                "label": "CTRY",
                "pattern": [
                    {"LOWER": "country"},
                    {"IS_PUNCT": True},
                    {"POS": "PROPN"}
                ]
            },
            {
                # webcam character
                "label": "WCCHAR",
                "pattern": [
                    {}, {}, {},
                    {"LOWER": {"IN": ["webcam", "webcams"]}},
                    {}, {}
                ]
            },
            {
                # potential facility
                "label": "PFAC",
                "pattern": [
                    {}, {},
                    {"LOWER": {
                        "IN": ["park", "library", "beach", "harbor", "harbour", "river", "lake", "zoo", "hospital",
                               "square"]}},
                    {}, {}
                ]
            }
        ]
        # 给EntityRuler添加模式
        ruler.add_patterns(patterns)
        doc = nlp(content)
        for tkn in doc.ents:
            if (tkn.label_ in ['GPE']):
                self.GPE_set.add(tkn.text)
            # print(tkn.text, " - ", tkn.label_)

    def extract_text_from_image(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
        }
        content = str()
        for img_src in self.img_list:
            try:
                urlf = urllib.request.urlopen(urllib.request.Request(img_src, headers = headers))
                image = Image.open(BytesIO(urlf.read()))
                text = self.reader.readtext(image, detail = 0)
                for i in text:
                    content += " " + i + " "
                # print(text)
            except:
                continue
        return content

    # Extract <title> <meta> <href>? and snapshot of img
    def extract_info(self, soup: BeautifulSoup):
        content = ""
        title_list = soup.find_all("title")
        meta_list = soup.find_all("meta")

        for tag in title_list:
            raw_str = tag.string
            processed_str = raw_str.replace('-', ' ')
            content += " " + processed_str + " "
        for tag in meta_list:
            if ("content" in tag.attrs):
                raw_str = tag.attrs['content']
                processed_str = raw_str.replace('-', ' ')
                content += " " + processed_str + " "

        # img_result = soup.find_all('img')
        # for tag in img_result:
        #     if ("src" in tag.attrs):
        #         img_url = tag.attrs['src']
        #         if (img_url.startswith("https")):
        #             self.img_list.append(img_url)

        # content += self.extract_text_from_image()
        self.find_geo_entity(content)

if __name__ == '__main__':
    web = "www.camhacker.com"
    file = "live-axis-webcam-1787-in-moscow-russian-federation.txt"
    # parser = web_parser(web, file)
    # parser.parse()
