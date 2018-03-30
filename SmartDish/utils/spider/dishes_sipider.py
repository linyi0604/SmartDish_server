import requests
from lxml import etree
import json
import os

class DishSpider(object):

    def __init__(self,url):
        self.url = url
        self.length = 0


    def get_html_code(self,url):
        response = requests.get(url=url,)
        code = response.text
        return code

    def get_url_list(self,html_code):
        elements = etree.HTML(html_code)
        url_list = elements.xpath('//div[@class="listtyle1"]/a/@href')
        return url_list

    def get_dish_list(self,url_list):
        dish_list = []
        for url in url_list:
            html_code = self.get_html_code(url)
            elements = etree.HTML(html_code)
            try:
                con = {
                    "name":elements.xpath('//a[@id="tongji_title"]/text()')[0] or "",
                    "features":elements.xpath('//dl[contains(@class,"yj_tags")]//text()') or "",
                    "labels":[ i.strip("#") for i in elements.xpath('//a[@class="curzt"]/text()')] or "",
                    "method":elements.xpath('//a[@id="tongji_gy"]/text()')[0] or "",
                    "taste":elements.xpath('//a[@id="tongji_kw"]/text()')[0] or "",
                    "detail":elements.xpath('//div[@class="materials"]/p/text()')[0] or "",
                    "image":elements.xpath('//div[@class="cp_headerimg_w"]/img/@src')[0] or "",
                }
                dish_list.append(con)
            except Exception as e:
                with open("error.log","a") as f:
                    f.write(str(e)+":"+url+"\n")
                continue

            self.length += 1
        return dish_list

    def get_next_page_code(self,html_code):
        elements = etree.HTML(html_code)
        next_url = elements.xpath('//a[@class="next"]/@href')
        if not next_url:
            return False
        else:
            next_url = next_url[0]
            print(next_url)
            return self.get_html_code(next_url)

    def save_file(self,con_list):
        for con in con_list:
            json_str = json.dumps(con,ensure_ascii=False)
            with open("./spiderData/dishes.json", "a") as f:
                f.write(json_str + "\n")


    def run(self):
        html_code = self.get_html_code(self.url)
        while html_code:
            url_list = self.get_url_list(html_code)
            dish_list = self.get_dish_list(url_list)
            html_code = self.get_next_page_code(html_code)
            self.save_file(dish_list)
            print("当前菜品数量:%s"%(self.length))





if __name__ == '__main__':
    if os.path.exists("./spiderData/dishes.json"):
        os.remove("./spiderData/dishes.json")
    if os.path.exists("./error.log"):
        os.remove("./error.log")
    target_list = [
        "http://www.meishij.net/hongpei/",
        "http://www.meishij.net/chufang/diy/guowaicaipu1/",
        "http://www.meishij.net/china-food/xiaochi/",
        "http://www.meishij.net/china-food/caixi/",
        "http://www.meishij.net/chufang/diy/",
    ]
    # spider = DishSpider(target_list[0])
    # spider.run()
    for url in target_list:
        spider = DishSpider(url)
        spider.run()