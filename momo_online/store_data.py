
from Model import Companys
from Public import BIASDataIO, Engine, PublicFun
from crawler_conf import CrawlerLogger
logger = CrawlerLogger()

def save_company_info(db_connection, company_info):
    print(company_info)
    company_guid = BIASDataIO.CheckCompanyMappingList(db_connection, company_info["factory_name"], NewCompanyGUID=False)
    if company_guid == "":
        company_guid = PublicFun.createID()
    try: companys = Engine.Query(db_connection, Companys.Companys(), "GUID=?", company_guid)
    except Exception as message: logger.logger.error(message)

    if companys.GUID == "":
        companys.GUID = company_guid
        companys.D_INSERTUSER = "MomoCrawler"
    else: companys.D_MODIFYUSER = "MomoCrawler"
    companys.Companys003 = company_info.get("factory_name",'')
    companys.Companys005 = company_info.get("factory_address",'')
    if not companys.Companys010 or "暫不提供" in companys.Companys010:
        companys.Companys010 = company_info.get("factory_phone",'')
    try: Engine.UpdateData(db_connection, companys)
    except Exception as message: logger.logger.error(message)
    return company_guid


def save_product_info(db_connection, company_guid, product_info, file_name):
    product_guid = check_product_info(db_connection, company_guid, product_info["product_name"])
    print(product_info)
    if not product_guid:
        insert_sql = ("INSERT INTO CompanyProduct(GUID, CompanyProduct001,CompanyProduct002,CompanyProduct003,CompanyProduct004,"
                      "CompanyProduct005,CompanyProduct006, CompanyProduct007, CompanyProduct008, D_INSERTUSER, D_INSERTTIME)"
                      " VALUES (?,?,?,?,?,?,?,?,?,?,?)")
        try:
            db_connection.Execute(insert_sql, (PublicFun.createID(),company_guid, "Momo", product_info.get("product_name",''), product_info.get("product_format",''),
                                  product_info.get("other_info",''), product_info.get("product_place",''), product_info.get("brand_name",''), file_name, "MomoCrawler", PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS")))
            logger.logger.info("Insert")
            print(file_name)
        except Exception as message:
            logger.logger.error(message); pass
    else:
        update_sql = "UPDATE CompanyProduct set CompanyProduct003=?,CompanyProduct004=?,CompanyProduct005=?,CompanyProduct006=?,CompanyProduct007=?,CompanyProduct008=?, D_MODIFYUSER=?, D_MODIFYTIME=? WHERE GUID = ?"
        try:
            db_connection.Execute(update_sql,(product_info.get("product_name",''), product_info.get("product_format",''),
                                  product_info.get("other_info",''), product_info.get("product_place",''), product_info.get("brand_name",''), file_name, "MomoCrawler", PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS"), product_guid))
            # logger.logger.info("Update")
        except Exception as message:
            logger.logger.error(message); pass


def check_product_info(db_connection, company_guid, product_name):
    query_sql = "SELECT GUID FROM CompanyProduct WHERE CompanyProduct001 = ? AND CompanyProduct002 = ? AND CompanyProduct003 = ?"
    rows = db_connection.GetDataTable(query_sql, (company_guid, "Momo", product_name))
    if rows: return rows[0][0]
    else: return ""
