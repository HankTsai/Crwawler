"""2021.02.05"""

import os
import time
import json
import random
from p_tqdm import p_imap
from varname.helpers import Wrapper
from multiprocessing.pool import ThreadPool
from Public import SQLConnect

"""載入程式運行的子函式"""
import definite_info as di
import selenium_funtion as sf
import store_data as sd
from crawler_conf import GeneralConfig, SaveAndRead, CrawlerLogger, RequestsConf

logger = CrawlerLogger()
config = GeneralConfig()
save_read = SaveAndRead()
request_conf = RequestsConf()


"""爬取所有產品分類的子網址，以便於獲得每種產品別中的所有品牌。"""
def get_primary_link():
    """find all categories data from host page."""
    try:
        home_page = request_conf.get_html(request_conf.home_url)
        sub_home_page = request_conf.get_html(home_page.xpath('//li[@id="C14"]//a/@href')[0])
        return sub_home_page
    except TypeError: pass
    except Exception as message:
        logger.logger.error(message)

def get_total_link():
    """get all link of categories from host page."""
    sub_list = {}
    sub_home_page = get_primary_link()
    try:
        for part in sub_home_page.xpath('//td'):
            sub_group = {}
            group_name = part[0].xpath('text()')
            for item in part[1]:
                name = item[0].xpath('text()')[0]
                link = item[0].xpath('@href')[0]
                sub_group[name] = link
            sub_list[group_name[0]] = sub_group
        return sub_list
    except AttributeError:
        logger.logger.error('AttributeError:NoneType')

def get_target_link(target_link):
    """put data to prepared target dictionary and store."""
    sub_list = get_total_link()
    for sub_target in target_link.values():
        for name, link in sub_list.items():
            if name in list(sub_target.keys()):
                sub_target[name] = link
    target_link_file = Wrapper(target_link)
    save_read.store_json(target_link, target_link_file.name)


"""獲得各類別中的所有大品牌名稱"""
def get_target_brand(target_brand):
    """crawl brand name by target dictionary."""
    for cate_name, cate_value in target_brand.items():
        same_categories = []
        for sub_name, sub_cate in cate_value.items():
            for name, link in sub_cate.items():
                single = sf.selenium_get_target_brand(name, link)
                try: same_categories.extend(single)
                except TypeError: pass
                except Exception as message: 
                    logger.logger.error(message)
                time.sleep(random.randint(1, 5))
        same_categories = set(same_categories)
        target_brand[cate_name] = list(same_categories)
    target_brand_file = Wrapper(target_brand)
    save_read.store_json(target_brand, target_brand_file.name)


"""藉由目標品牌名單，爬取所有各品牌旗下產品網址"""
def stage_store(brand_link_dict,brand_name):
    while True:
        try:
            os.system('pkill chrome')
            logger.logger.info('The driver has been quit.')
            logger.logger.info(f'got number of brand_links is {len(brand_link_dict)}.')
            save_read.store_json(brand_link_dict, brand_name)
            break
        except Exception as message:
            logger.logger.info(f'because of {message}, {brand_name}\'s storing failed.')
            ans = input('do you want to try again?(y/n)')
            if ans =="y": continue
            else: break

def get_product_link(file):
    """get every product link from each brand."""
    brand_dict = save_read.read_json(file)
    for cate_name, brand_list in brand_dict.items():
        sub_cate_dict = {}
        name = config.cate_type[cate_name]
        tmp_brand_link = ThreadPool(8).map(sf.selenium_get_product_link,brand_list)
        for brand, links in zip(brand_dict, tmp_brand_link):
            sub_cate_dict[brand] = links
        stage_store(sub_cate_dict,name)


"""擷取各產品網址的細項內容。"""
def check_target_file(product_type):
    for file in os.listdir('file'):
        if product_type:
            if f"{product_type}" in file:
                return file
        else:
            if "product_" in file:
                return file

def get_product_info(product_type):
    """get product info from each product link."""
    file = check_target_file(product_type)
    product_links = save_read.read_json(file)
    for brand, links in product_links.items():
        if links:
            for link in links:
                if link:
                    company_info, product_info = di.definite_detail_info(link)
            # info = ThreadPool(6).map(di.definite_detail_info, [link for link in links if link])
                    store_to_db(company_info, product_info)
        logger.logger.info(f"Save {brand}")
        time.sleep(random.randint(1, 5))


"""分成廠商與產品兩類資訊各自存入DB"""
def store_to_db(company_info, product_info):
    """store info to DB by company and product."""
    db_connection = SQLConnect.DBConnect(publicSetting=True)
    db_connection.ConnectDB()
    if company_info.get("factory_name",''):
        company_guid = sd.save_company_info(db_connection, company_info)
        # logger.logger.info("Save Company:" + company_info["factory_name"])
        if product_info.get("product_name",''):
            sd.save_product_info(db_connection, company_guid, product_info)
            # logger.logger.info("Save Product:" + product_info["product_name"])



def main():
    logger.store_logger()
    # get_target_link(config.target)
    # get_target_brand(config.target)
    # get_product_link(config.brand_file)
    get_product_info(config.point_type)


if __name__ == '__main__':
    main()


