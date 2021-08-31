
import re
import time
import random
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from crawler_conf import GeneralConfig, SaveAndRead, CrawlerLogger, RequestsConf
logger = CrawlerLogger()
config = GeneralConfig()
save_read = SaveAndRead()
request_conf = RequestsConf()


def get_driver():
    """selenium driver setting."""
    driver = getattr(config.threadloacl, 'driver', None)
    if driver is None:
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        options.add_argument('blink-settings=imagesEnabled=false')
        options.add_argument(f'user-agent={config.random_ua()}')
        pref = {'profile.default_content_setting_values': {'notifications': 2}}
        options.add_experimental_option('prefs', pref)
        driver = webdriver.Chrome('./chromedriver', options=options)
        setattr(config.threadloacl, 'driver', driver)
    return driver

def selenium_get_target_brand(error_name, url):
    """use selenium to get brand from target_link."""
    for _ in range(3):
        num = 0
        driver = get_driver()
        try:
            driver.get(url)
            WebDriverWait(driver, 6).\
                until(expected_conditions.
                    presence_of_element_located((By.CLASS_NAME, 'openMoreBtn'))).click()
            brand_show = driver.find_elements_by_xpath('//li[@class="cateS"]//h2//label')
            brand_hide = driver.find_elements_by_xpath('//li[@class="cateS hide"]//h2//label')
            brand = [item.text for item in brand_show+brand_hide]
            logger.logger.info(error_name)
            return brand
        except WebDriverException as message:
            logger.logger.error(f'{error_name}:{message}')
            num = num + 1
            random.seed(num)
    return None

def selenium_get_brand_page(name):
    """choose which brand name will be searched"""
    times = 1
    while times <= 3:
        try:
            driver = get_driver()
            driver.get(request_conf.search_url + name)
            WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'brandBtn'))).click()
            WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="brandBox sameFloatType"]//ul//li[1]'))).click()
            WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'determineBtn'))).click()
            return driver
        except: times += 1
    logger.logger.error(f'pass {name} search')
    return None

def selenium_get_product_link(brand):
    """scrape brand's all link of product"""
    tmp_brand_link = []
    turn_page = True
    driver = selenium_get_brand_page(brand)
    if not driver: return None

    while turn_page:
        time.sleep(2)
        try:
            html = etree.HTML(driver.page_source)
            product_link = html.xpath('//article[@class="prdListArea"]//li//a/@href')
            for link in product_link:
                tmp_brand_link.append(request_conf.mobile_url + link)
            cur_page = re.search(r'curPage=\d+', driver.current_url).group(0)
            max_page = re.search(r'maxPage=\d+', driver.current_url).group(0)
            if not cur_page[8] == max_page[8]:
                page = driver.find_element_by_xpath('//div[@class="pageArea"]//dl//dt[@id="rightBtn"]//a')
                driver.execute_script("arguments[0].scrollIntoView(true);", page)
                WebDriverWait(driver, 2).until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, '//div[@class="pageArea"]//dl//dt[@id="rightBtn"]//a'))).click()
            else: turn_page = False
        except Exception as e:
            logger.logger.warning(f'{brand} page may miss')
            logger.logger.error(e)
            turn_page = False

    if tmp_brand_link:
        logger.logger.info(f'{brand} / {len(tmp_brand_link)}')
        return tmp_brand_link
    else: return []
