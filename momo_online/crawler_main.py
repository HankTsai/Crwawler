"""2021.02.05"""

import os
import time
import sys
import json
import argparse
import random
from datetime import datetime
from varname.helpers import Wrapper
from multiprocessing.dummy import Pool as ThreadPool
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
    """將小分類的頁面連結放入config.target的字典中"""
    sub_list = get_total_link()
    for sub_target in target_link.values():
        for name, link in sub_list.items():
            if name in list(sub_target.keys()):
                sub_target[name] = link
    # target_link = {'日常用品': {'個人用品': {'衛生紙': 'httpsxxxx,'濕紙巾':'httpxxxx'...},{'家用清潔':{'洗衣精/粉':'httpxxxxx'}}


def get_target_brand(target_brand):
    """根據config.target爬取每個分類中的所有品牌名稱"""
    for cate_name, cate_value in target_brand.items():
        same_categories = []
        for sub_name, sub_cate in cate_value.items():
            for name, link in sub_cate.items():
                # example :  name = 衛生紙, link = https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=3900100000&mdiv=1099600000-bt_0_996_19-&ctype=B
                single = sf.selenium_get_target_brand(name, link)
                try:same_categories.extend(single)
                except TypeError: pass
                except Exception as message:
                    logger.logger.error(message)
                time.sleep(random.randint(1, 5))
        same_categories = set(same_categories)
        target_brand[cate_name] = list(same_categories)
    # target_brand = {'日常用品': ['OLDAM', '雷達', 'Simple Real', '你會買'....],美妝清潔....
    # 品牌的統整變回只分三大類 : 日常用品、美妝清潔、食品飲料。


def stage_store(brand_link_dict,brand_name):
    """設定每個網址的儲存"""
    repeat = True
    again = 1
    while repeat:
        try:
            os.system('pkill chrome')
            logger.logger.info('The driver has been quit.')
            logger.logger.info(f'got number of brand_links is {len(brand_link_dict)}.')
            save_read.store_json(brand_link_dict, brand_name)
            repeat = False
        except Exception as message:
            logger.logger.info(f'because of {message}, {brand_name}\'s storing failed.')
            if again <= 3:
                again += 1
                continue
            else: repeat = False

def get_product_link(brand_names):
    """藉由目標品牌名單，爬取所有各品牌旗下產品網址"""
    for cate_name, brand_list in brand_names.items():
        sub_cate_dict = {}
        name = config.cate_file_name[cate_name]
        tmp_brand_link = ThreadPool(3).map(sf.selenium_get_product_link,brand_list)
        for brand, links in zip(brand_names[cate_name], tmp_brand_link):
            sub_cate_dict[brand] = links
        stage_store(sub_cate_dict,name)


def check_target_category(target_type):
    """擷取各產品網址的細項內容。"""
    file_list = []
    for file in os.listdir('file'):
        if len(target_type)>0:
            if f"{target_type}" in file:
                file_list.append(file)
                logger.logger.info(f'指定類別資料存在，準備針對{file}做產品資訊爬取...')
        else:
            if "product" in file:
                file_list.append(file)
                logger.logger.info(f'無指定項目，準備針對{file}做產品資訊爬取...')
    return file_list


def get_product_info(brand_product_links,file_name):
    """從每一個單一品項獲得所需資訊"""
    for brand, links in brand_product_links.items():
        try:
            print(f'start {brand} crawl')
            if len(links) >= 1:
                info_list = ThreadPool(4).map(di.definite_detail_info, [link for link in links if link])
                # for link in links:
                #     if link:
                #         info = di.definite_detail_info(link)
                for info in info_list:
                    store_to_db(info[0], info[1], file_name,brand)
                time.sleep(random.randint(1, 3))
        except TypeError:
            logger.logger.warning(f'{brand} is None')
            pass


"""分成廠商與產品兩類資訊各自存入DB"""
def store_to_db(company_info, product_info, file_name,brand):
    """將資訊導入DB中"""
    db_connection = SQLConnect.DBConnect(publicSetting=True)
    db_connection.ConnectDB()
    """如果沒有廠商資訊，則不會存入該產品(代表對於銷售沒有意義)"""
    if company_info.get("factory_name",''):
        company_guid = sd.save_company_info(db_connection, company_info)
        if product_info.get("product_name",''):
            sd.save_product_info(db_connection, company_guid, product_info, file_name)
            logger.logger.info(f"{brand} info saved")

def params_input():
    """程式啟動參數設定"""
    parser = argparse.ArgumentParser(description="target type para setting. ")
    parser.add_argument('-t', type=str, default='', help='if you need specific type of production, you can key-in here.')
    args = parser.parse_args()
    return args.t

def main():
    logger.store_logger()
    target_type = params_input()
    while True:
        file_list = check_target_category(target_type)
        if len(file_list) > 0:
            for file in file_list:
                if len(file) > 0:
                    brand_product_links = save_read.read_json(file)
                    get_product_info(brand_product_links, file[8:-5])
            break
        else:
            logger.logger.info('file資料夾中不存在類別的產品鏈接，開始重新爬取...')
            get_target_link(config.target)
            get_target_brand(config.target)
            get_product_link(config.target)



if __name__ == '__main__':
    main()


