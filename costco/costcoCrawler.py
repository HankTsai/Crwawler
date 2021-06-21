import datetime
import logging
import os
import time
import json

from bs4 import BeautifulSoup

import CatchCostcoUtil
from Model import Companys
from Public import SQLConnect, BIASDataIO, Engine, PublicFun


session = None
header = None
logger = None
base_url = "https://www.costco.com.tw"
    
def create_logger() :
    """建位log物件
    """
    global logger
    logPath = "logs/" + datetime.datetime.now().strftime("Costco_%Y-%m-%d_%H-%M-%S.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(os.path.basename(__file__))
    hander = logging.FileHandler(logPath, "w", encoding = "UTF-8")
    hander.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(hander)
    #增加顯示在console裡的log
    # consoleHandler = logging.StreamHandler()
    # consoleHandler.setFormatter(formatter)
    # logger.addHandler(consoleHandler)

def get_category_url(base_url, json_data):
    """找到"產品類別"
    """
    result_list = []
    #找到"產品類別"
    category = json_data["category"]
    for sub_categpry in category["subCategories"]:
        #改版後可使用web api取得資料, 所以只要記錄code就可以
        result_list.append(sub_categpry["code"])
#     category_soup = soup.find("div", class_ = "category-wrapper")
#     category_soup_list = category_soup.findAll("div", class_ = "category-node ng-star-inserted")
#     logger.info(category_soup_list)
#     for nod_soup in category_soup_list:
#         category_url = base_url + nod_soup.find("a", class_ = "category-link ng-star-inserted")["href"]
#         result_list.append(category_url)
    return result_list

def get_product_url(base_url, soup):
    """取得類別裡的產品內容
    """
#     result_list = []
    #找到"產品列表"
    product_view_soup = soup.find(id = "list-view-id")
    product_soup_list = product_view_soup.findAll("li", recursive="False")
    for item_soup in product_soup_list:
        link_list = item_soup.findAll("a")
        item_url = base_url + link_list[0]["href"]
        try:
            get_company_info_from_product(item_url)
        except Exception as e:
            logger.error("URL:" + item_url)
            logger.error(e)
#         result_list.append(item_url)
#     return result_list

def create_default_product():
    result= {}
    result["NAME"] = ""
    result["SPEC"] = ""
    result["INGREDIENT"] = ""
    result["ORIGIN"] = ""
    return result

def create_default_comapny():
    result= {}
    result["NAME"] = ""
    result["TEL"] = ""
    result["ADDRESS"] = ""
    return result

def get_company_info_from_product(product_url):
    """取得製造/進口商資料
    """
    product_info = create_default_product()
    company_info = create_default_comapny()
    logger.info("Product:" + product_url)
    resp = CatchCostcoUtil.send_get_request(logger, session, product_url, header)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "lxml")
    #商品規格
    product_specs_soup = soup.find("div", id = "collapse-PRODUCT_SPECS")
    product_table = product_specs_soup.find("table")
    for specs_soup in product_table.findAll("tr"):
        name = specs_soup.find("td", class_ = "attrib").text.strip(" \t\n\r")
        value_soup = specs_soup.find("td", class_ = "attrib-val")
        value = value_soup.text.strip(" \t\n\r")
        if "品名" in name:
            product_info["NAME"] = value
        elif "內容量/入數" in name:
            product_info["SPEC"] = value
        elif "成分" in name:
            product_info["INGREDIENT"] = value
        elif "產地" in name:
            product_info["ORIGIN"] = value
        elif "製造/進口商名稱" in name:
            company_info["NAME"] = get_taiwan_company_info(value_soup)
        elif "製造/進口商電話" in name:
            company_info["TEL"] = value
        elif "製造/進口商地址" in name:
            company_info["ADDRESS"] = get_taiwan_company_info(value_soup)
    db_connection = SQLConnect.DBConnect(publicSetting=True)
    db_connection.ConnectDB()
    logger.info("Save Company:" + company_info["NAME"])
    if company_info["NAME"] is not None and len(company_info["NAME"]) > 0:
        company_guid = save_company_info(db_connection, company_info)
        logger.info("Save Product:" + product_info["NAME"])
        save_product_info(db_connection, company_guid, product_info)
    time.sleep(2)
    
def get_taiwan_company_info(info_soup):
    result = ""
    if "進口商" in info_soup.text:
        tmp_text = info_soup.text
        if info_soup.findAll("p"):
            for info in info_soup.findAll("p") :
                if "進口商" in info.text:
                    tmp_text = info.text
            
        if ":" in tmp_text:
            result = tmp_text.split(":")[1]
        else:
            result = tmp_text.split("：")[1]
        
    else:
        result = info_soup.text.strip(" \t\n\r")
    return result

def save_company_info(db_connection, company_info):
    """新增或更新公司資訊
    """
    company_guid = BIASDataIO.CheckCompanyMappingList(db_connection,company_info["NAME"],NewCompanyGUID=False)
    if company_guid == "":
        company_guid= PublicFun.createID()
    companys = Engine.Query(db_connection,Companys.Companys(),"GUID=?", (company_guid,))
    
    if companys.GUID =="":
        companys.GUID=company_guid
        companys.D_INSERTUSER="CostcoCrawler"
    else:
        companys.D_MODIFYUSER="CostcoCrawler"
    companys.Companys003 = company_info["NAME"]
    companys.Companys005 = company_info["ADDRESS"]
    if companys.Companys010 == None or len(companys.Companys010) == 0 or "暫不提供" in companys.Companys010 :
        companys.Companys010 = company_info["TEL"]
    Engine.UpdateData(db_connection,companys)
    return company_guid
    
def save_product_info(db_connection, company_guid, product_info):
    """新增產品資訊
    """
    product_guid = check_product_info(db_connection, company_guid, product_info["NAME"])
    if len(product_guid)  == 0:
        logger.info("Insert")
        insert_sql = ("INSERT INTO CompanyProduct(GUID, CompanyProduct001,CompanyProduct002,CompanyProduct003,CompanyProduct004,CompanyProduct005,CompanyProduct006, D_INSERTUSER, D_INSERTTIME)"
                      " VALUES (?,?,?,?,?,?,?,?,?)")
        db_connection.Execute(insert_sql, (PublicFun.createID(), company_guid, "Costco", product_info["NAME"], product_info["SPEC"], product_info["INGREDIENT"]
                                           , product_info["ORIGIN"], "CostcoCrawler", PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS")))
    else:
        logger.info("Update")
        update_sql = "UPDATE CompanyProduct set D_MODIFYUSER = ?, D_MODIFYTIME = ? WHERE GUID = ?"
        db_connection.Execute(update_sql, ("CostcoCrawler", PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS"), product_guid))
    
def check_product_info(db_connection, company_guid, product_name):
    """檢查產品資訊是否已存在
    """
    query_sql = "SELECT GUID FROM CompanyProduct WHERE CompanyProduct001 = ? AND CompanyProduct002 = ? AND CompanyProduct003 = ?"
    rows = db_connection.GetDataTable(query_sql, (company_guid, "Costco", product_name))
    if rows is not None and len(rows) > 0:
        return rows[0][0]
    else:
        return ""
            
def get_category_product_url(api_url, category_url):
    """取得category裡的每一頁的內容
    """
    #改版後直接從web api取得資料
    total_page_count = 1
    next_page = 1
    while next_page <= total_page_count:
        resp = CatchCostcoUtil.send_get_request(logger, session, api_url + "&category=" + category_url, json_header)
        resp.encoding = "utf-8"
        logger.info("Page:" + str(next_page))
        json_data = json.loads(resp.text)
        total_page_count = json_data["pagination"]["totalPages"]
        logger.info("totalPages:" + str(total_page_count))
        for product_info in json_data["products"]:
            procudt_url = base_url + product_info["url"]
#             logger.info(procudt_url)
            try:
                get_company_info_from_product(procudt_url)
            except Exception as e:
                logger.error("URL:" + procudt_url)
                logger.error(e)
        next_page += 1
        
    """
    page_url = category_url
    while page_url is not None:
        logger.info("Page:" + page_url)
        resp = CatchCostcoUtil.send_get_request(logger, session, page_url, header)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "lxml")
        get_product_url(base_url, soup, logger)
        page_soup = soup.find("ul", class_ = "pagination notranslate")
        if page_soup :
            page_list_soup = page_soup.findAll("li")
            next_page_soup = page_list_soup[-1]
            #有找到link代表有下一頁, 若是最後一頁就不會有
            if next_page_soup.find("a"):
                page_url = base_url + next_page_soup.find("a")["href"]
            else:
                page_url = None
        else:
            page_url = None
    """
    
def get_food_data():
    api_base_url = base_url + "/rest/v2/taiwan/products/search?fields=FULL&query=&pageSize=300&lang=zh_TW&curr=TWD"
    #食品類的網頁
    resp = CatchCostcoUtil.send_get_request(logger, session, api_base_url + "&category=8", json_header)
    resp.encoding = "utf-8"
    json_data = json.loads(resp.text)
#     logger.info(json_data)
#     soup = BeautifulSoup(resp.text, "lxml")
    category_url_list = get_category_url(base_url, json_data)
    for category_url in category_url_list:
        logger.info("Category:" + category_url)
        get_category_product_url(api_base_url, category_url)

def main():
    global session, header, json_header
    create_logger()
    session = CatchCostcoUtil.get_session()
    header = CatchCostcoUtil.get_header_with_hostname("www.costco.com.tw")
    json_header = header
    json_header["accept"] = "application/json, text/plain, */*"
    json_header["content-type"] = "application/json"
    json_header["referer"] = "https://www.costco.com.tw/Food/c/8"
    get_food_data()
#     get_company_info_from_product("https://www.costco.com.tw/Food/Snacks/Chocolates-Candies-Jelly/Glico-Pocky-Chocolate-Biscuit-Sticks-40G-X-12-Count/p/103454")


    

#主要執行邏輯
if __name__ == "__main__":
    main()