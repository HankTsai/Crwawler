import sys
import time
from bs4 import BeautifulSoup as bs

from selenium.webdriver.common.action_chains import ActionChains

import Public.PublicFun as PublicFun
import Public.SQLConnect as SQLConnect
import Public.BIASDataIO as BIASDataIO

DBConnect=None
JobID=""
try:
    JobID=sys.argv[1]
    DBConnect=SQLConnect.DBConnect(publicSetting=True)
    DBConnect.ConnectDB()
    DBConnect.StartTransaction()
    
    Chromedriver=PublicFun.getWebDriver("chrome",DataFolderName=JobID)
    Chromedriver.get("https://www.104.com.tw/jobs/search/")

    #找到職務類別的按鈕並點擊
    CategoryListButton=Chromedriver.find_element_by_id("job-cat")
    ActionChains(Chromedriver).click(CategoryListButton).perform()
    time.sleep(5)

    e104menu=Chromedriver.find_element_by_id("e104menu2011_main")
    e104menuCount = len(bs(e104menu.get_attribute('innerHTML'), "html.parser").select("ul li"))

    #逐項取得內容
    for ClassACount in range(e104menuCount):
        #移開選取項目
        tempElement=Chromedriver.find_element_by_id("globalbar")
        ActionChains(Chromedriver).move_to_element(tempElement).perform()
        time.sleep(2)

        #滑鼠移至項目
        tempElement=Chromedriver.find_element_by_id("e104menu2011_m_i_"+str(ClassACount))
        ActionChains(Chromedriver).move_to_element(tempElement).perform()
        time.sleep(1)
        CategoryContent=Chromedriver.find_element_by_id("e104menu2011_sub").get_attribute("innerHTML")
        CategoryContent=bs(CategoryContent, "html.parser")

        ClassA=CategoryContent.select("h1 label")[0].text
        ClassAGUID = BIASDataIO.insertOption(DBConnect,ClassA)
        for tempSoup in CategoryContent.select("ul"):
            ClassB=tempSoup.select("li.e104menu2011_sut")
            if ClassB is None or len(ClassB)==0:
                ClassB=ClassA
            else:
                ClassB=ClassB[0].select("label")[0].text
            ClassBGUID = BIASDataIO.insertOption(DBConnect,ClassB,ClassAGUID)
            
            for tempSoup2 in tempSoup.select("li.e104menu2011_txt label"):
                BIASDataIO.insertOption(DBConnect,tempSoup2.text,ClassBGUID)
                    
    closeButton=Chromedriver.find_element_by_id("e104menu2011_box").find_element_by_xpath("h1/span")
    ActionChains(Chromedriver).click(closeButton).perform()

    #切換高階職類
    CategoryListButton=Chromedriver.find_element_by_id("job-type")
    ActionChains(Chromedriver).click(CategoryListButton).perform()

    #找到職務類別的按鈕並點擊
    CategoryListButton=Chromedriver.find_element_by_id("job-cat")
    ActionChains(Chromedriver).click(CategoryListButton).perform()
    time.sleep(5)

    e104menu=Chromedriver.find_element_by_id("e104menu2011_main")
    e104menuCount = len(bs(e104menu.get_attribute('innerHTML'), "html.parser").select("ul li"))

    #逐項取得內容
    for ClassACount in range(e104menuCount):
        #移開選取項目
        tempElement=Chromedriver.find_element_by_id("globalbar")
        ActionChains(Chromedriver).move_to_element(tempElement).perform()
        time.sleep(2)

        #滑鼠移至項目
        tempElement=Chromedriver.find_element_by_id("e104menu2011_m_i_"+str(ClassACount))
        ActionChains(Chromedriver).move_to_element(tempElement).perform()
        time.sleep(1)
        CategoryContent=Chromedriver.find_element_by_id("e104menu2011_sub").get_attribute("innerHTML")
        CategoryContent=bs(CategoryContent, "html.parser")

        ClassA=CategoryContent.select("h1 label")[0].text
        ClassAGUID = BIASDataIO.insertOption(DBConnect,ClassA)
        for tempSoup in CategoryContent.select("ul"):
            ClassB=tempSoup.select("li.e104menu2011_sut")
            if ClassB is None or len(ClassB)==0:
                ClassB=ClassA
            else:
                ClassB=ClassB[0].select("label")[0].text
            ClassBGUID = BIASDataIO.insertOption(DBConnect,ClassB,ClassAGUID)
            
            for tempSoup2 in tempSoup.select("li.e104menu2011_txt label"):
                BIASDataIO.insertOption(DBConnect,tempSoup2.text,ClassBGUID)
                    
    closeButton=Chromedriver.find_element_by_id("e104menu2011_box").find_element_by_xpath("h1/span")
    ActionChains(Chromedriver).click(closeButton).perform()

    DBConnect.commit()
except Exception as ex:
    DBConnect.rollback()
    print("")
PublicFun.closeWebDriver(JobID,Chromedriver)
DBConnect.close()
