import scrapy

from AoiSolas.items import AoisolasItem
from bs4 import BeautifulSoup


class AoisolaspiderSpider(scrapy.Spider):
    name = 'pic'
    allowed_domains = ['www.youzi4.cc']
    start_urls = ['http://www.youzi4.cc/rihanmeinv/',
                  # 'http://www.youzi4.cc/siwameitui/',
                  # 'http://www.youzi4.cc/xiaoqingxinmeinv/'
                  ]

    def parse(self, response):
        # print(response.text)
        data = response.body
        soup = BeautifulSoup(data, 'lxml')

        list = soup.find_all('li', {'class': 'wenshens'})
        next_page = soup.find('a', {'class': 'next-page-a'})
        for l in list:
            l_url = str('http://www.youzi4.cc' + l.find('a', {'target': '_blank'}).get('href'))
            if next_page is not None:
                 next_page_url = next_page.get('href')
                 #获取下一页里的图片合集url
                 yield response.follow(next_page_url,callback=self.parse)
            yield scrapy.Request(l_url, callback=self.content)


    def content(self, response):
        item = AoisolasItem()
        data = response.body
        soup = BeautifulSoup(data, 'lxml')
        title = soup.find('h1', {'class': 'articleV4Tit'}).get_text()
        img_url = soup.find('img', {'class': 'IMG_show'}).get('src')

        img_urls = []
        #titles.append(title)
        img_urls.append(img_url)
        item['title'] = title
        item['ImgUrl'] = img_urls
        yield item
        next_page = soup.find('a', {'class': 'next-page-a'})
        if next_page is not None:
            next_page_url = next_page.get('href')

            yield response.follow(next_page_url, callback=self.content)
