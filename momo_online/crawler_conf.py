
import os
import json
import time
import random
import datetime
import logging
import requests
import threading
from lxml import etree
from requests.adapters import HTTPAdapter
from fake_useragent import UserAgent
random.seed(1)


class CrawlerLogger:
    def __init__(self):
        """make logger"""
        self.logger = logging.getLogger(os.path.basename(__file__))
        self.formatter = logging.Formatter(
            '["%(asctime)s - %(levelname)s - %(name)s - %(message)s" - function:%(funcName)s -  line:%(lineno)d]')
        logging.basicConfig(level=logging.INFO, datefmt='%Y%m%d_%H:%M:%S',)

    def store_logger(self):
        """definite log"""
        log_path = "log/" + datetime.datetime.now().strftime("momo_%Y-%m-%d_%H-%M-%S.log")
        handler = logging.FileHandler(log_path, "w", encoding = "UTF-8")
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def show_logger(self):
        console = logging.StreamHandler()
        console.setLevel(logging.FATAL)
        console.setFormatter(self.formatter)
        self.logger.addHandler(console)


class GeneralConfig:
    """set general config"""
    def __init__(self):
        self.fake_agents = [UserAgent().random for _ in range(10)]
        # self.fake_proxy = [fake_proxy.get(proxy_type='https',amount=10)]
        self.random_ua = lambda: random.sample(self.fake_agents, 1)[0]
        # self.random_ip = lambda: random.sample(self.fake_proxy,1)[0][0]
        self.threadloacl = threading.local()
        self.total_brand_link = {}
        self.cate_type = {'日常用品':'daily_necessities','美妝清潔':'cosmetic_clean','食品飲料':'food_drink'}
        self.brand_file = 'target_brand_file.json'
        self.point_type = "product_food_drink"
        self.target = {"日常用品": {'個人用品': {}, '家用清潔': {}, '生活百貨': {}, '餐廚用品': {}},
                       "美妝清潔": {'臉部保養': {}, '彩妝/用品': {}, '香氛/SPA': {}, '身體/嬰幼保養': {}, '個人清潔': {}, '洗髮沐浴': {}, '洗臉/口腔': {}},
                       "食品飲料": {'養生/保健': {}, '零食/點心': {}, '飲料/沖泡': {}, '民生食材/南北貨': {}, '生鮮/低溫': {}}}

# GeneralConfig().fake_proxy
# print(GeneralConfig().random_ip())

class RequestsConf:
    """set requests config"""
    def __init__(self):
        self.home_url = 'https://www.momoshop.com.tw/main/Main.jsp?'
        self.search_url = 'https://m.momoshop.com.tw/search.momo?searchKeyword='
        self.mobile_url = 'https://m.momoshop.com.tw'
        self.session = requests.Session()
        self.connect_error = 0
        # self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.headers = {'User-Agent': GeneralConfig().random_ua(),
                   'authority': 'www.momoshop.com.tw',
                   'method': 'GET',
                   'path': '/main/Main.jsp',
                   'scheme': 'https',
                   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'accept-encoding': 'gzip, deflate, br',
                   'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                   'cache-control': 'max-age=0',
                   'cookie': 'CAD=1; _ga=GA1.3.145003070.1611816453; __auc=f8a6ec7817747bf424c74a40a89; _mwa_uniCampaignInfo=1611816452747274614.1611816452747; firstTimeOpenShop=forever; ARK_ID=JSa7a81661197d6865d6f6d81706f66906a7a8; _atrk_siteuid=nNzHZ1fwdz9f6EGi; _tam=F_k4NmiMATKWrE8-B3S0nOCA; _fbp=fb.3.1611816459469.1301332957; appier_utmz=%7B%22csr%22%3A%22www.momoshop.com.tw%22%2C%22timestamp%22%3A1611816459%2C%22lcsr%22%3A%22www.momoshop.com.tw%22%7D; _gid=GA1.3.886555289.1612071619; GoodsBrowsingHistory=6173730_1588386256/3631231_1611774844/5615812_1583499607/6246238_1611599666; JSESSIONID=A2D0A2F88897B4923BF2955A673D036F-m1.shop46; wshop=wshop_web_a_46; _gat=1; _mwa_uniVisitorInfo=1611816452744751951.1611816452744.23.1612316651855; __asc=4039a73e177658fb358b5035446; bid=af53413bb390673411f9962f6d0f7d16; isBI=1; _atrk_ssid=i9SNqBbxn5Rv3xQW3gcGxR; _atrk_sessidx=2; appier_pv_counterERlDyPL9yO7gfOb=0; appier_page_isView_ERlDyPL9yO7gfOb=f42a524e779bd74dc4d8c3f4c7cf713fea37ab2fbf23e346b8d74d9359dc7aea; _gat_gtag_UA_22652017_1=1; TN=undefined; CN=undefined; CM=undefined; _mwa_uniSessionInfo=1612316651854599231.1612316651854.5.1612316658064',
                   'referer': 'https://www.momoshop.com.tw/',
                   'sec-fetch-dest': 'document',
                   'sec-fetch-mode': 'navigate',
                   'sec-fetch-site': 'same-origin',
                   'sec-fetch-user': '?1',
                   'upgrade-insecure-requests': '1'}

    def get_html(self, url):
        """requests.get setting """
        for _ in range(3):
            try:
                respond = self.session.get(url=url,headers=self.headers, timeout=8)
                html = etree.HTML(respond.text)
                self.connect_error = 0
                return html
            except Exception as message:
                self.connect_error += 1
                if self.connect_error == 5:
                    random.seed(random.randint(1,100))
                    self.headers['User-Agent'] = GeneralConfig().random_ua()
                    print(self.headers['User-Agent'])
                    time.sleep(5)
                CrawlerLogger().logger.error(message)
        return None


class SaveAndRead:
    def __init__(self):
        self.filepath = "file"

    def store_json(self, dict_file, filename):
        CrawlerLogger().show_logger()
        with open(f'{self.filepath}/{filename}.json', 'w') as file:
            file.write(json.dumps(dict_file))
        CrawlerLogger().logger.info('file stored.')

    def read_json(self, filename):
        with open(f'{self.filepath}/{filename}', 'r') as file:
            return json.loads(file.read())





