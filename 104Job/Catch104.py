import sys
from bs4 import BeautifulSoup as bs
import datetime
import time

import Public.PublicFun as PublicFun
import Public.RequestsHandler as RequestsHandler
import Public.SettingReader as SettingReader
import Public.QueueIO as QueueIO
import Public.LogHandler as LogHandler

def getPageSize(requestURL):
    JobID=PublicFun.createID()
    Chromedriver=PublicFun.getWebDriver("chrome",DataFolderName=JobID)
    Chromedriver.get(requestURL)
    
    time.sleep(2)
    Soup = bs(Chromedriver.page_source, "html.parser")
    pageSize=len(Soup.select("select.b-clear-border.js-paging-select.gtm-paging-top option"))
    if pageSize==0:
        pageSize=len(Soup.select("select.page-select.js-paging-select.gtm-paging-top option"))
    PublicFun.closeWebDriver(JobID,Chromedriver)
    return pageSize

if __name__ == '__main__':
    jsondata=""
    try:
        JobID=sys.argv[1]
        data=sys.argv[2]
        jsondata = PublicFun.StringToJson(data)
        if "UpdateJobCategory" in jsondata and str(jsondata["UpdateJobCategory"])=="True":
            UpdateJobCategoryQueue=QueueIO.setParameter("","")
            UpdateJobCategoryPath=SettingReader.getSetting("excutePath","UpdateJobCategory")
            QueueIO.addQueue("Update104JobCategory","Excute",UpdateJobCategoryPath,"UpdateJobCategory.py",UpdateJobCategoryQueue)
        
        requestHost=SettingReader.getSetting("global","requestHost")
        CatchListPath=SettingReader.getSetting("excutePath","CatchList")
        SearchURL=SettingReader.getSetting("global","searchURL")

        if "condition" in jsondata:
            jsondata=jsondata["condition"]
            if "jobcats" in jsondata:
                for jobcat in jsondata["jobcats"]:
                    condition="&jobcat="+jobcat        
                    JobWebSite=SearchURL+condition
                    pageSize=getPageSize(JobWebSite+"&page=1")
                    for n in range(pageSize):
                        CatchListQueue=QueueIO.setParameter("URL",JobWebSite+"&page="+str(n+1))
                        QueueIO.addQueue("JobList","Excute",CatchListPath,"CatchList.py",CatchListQueue)
            
            if "KeyWords" in jsondata:
                for KeyWord in jsondata["KeyWords"]:
                    condition="&keyword="+KeyWord        
                    JobWebSite=SearchURL+condition
                    pageSize=getPageSize(JobWebSite+"&page=1")
                    for n in range(pageSize):
                        CatchListQueue=QueueIO.setParameter("URL",JobWebSite+"&page="+str(n+1))
                        QueueIO.addQueue("JobList","Excute",CatchListPath,"CatchList.py",CatchListQueue)

            if "Areas" in jsondata:
                for Area in jsondata["Areas"]:
                    condition="&area="+Area        
                    JobWebSite=SearchURL+condition
                    pageSize=getPageSize(JobWebSite+"&page=1")
                    for n in range(pageSize):
                        CatchListQueue=QueueIO.setParameter("URL",JobWebSite+"&page="+str(n+1))
                        QueueIO.addQueue("JobList","Excute",CatchListPath,"CatchList.py",CatchListQueue)
            
            if "indcats" in jsondata:
                for indcat in jsondata["indcats"]:
                    condition="&indcat="+indcat        
                    JobWebSite=SearchURL+condition
                    pageSize=getPageSize(JobWebSite+"&page=1")
                    for n in range(pageSize):
                        CatchListQueue=QueueIO.setParameter("URL",JobWebSite+"&page="+str(n+1))
                        QueueIO.addQueue("JobList","Excute",CatchListPath,"CatchList.py",CatchListQueue)
        else:
            JobWebSite=SearchURL
            req=RequestsHandler.getNewRequests(JobWebSite+"&page=1",requestHost)
            pageSize=getPageSize(JobWebSite+"&page=1")
            for n in range(pageSize):
                CatchListQueue=QueueIO.setParameter("URL",JobWebSite+"&page="+str(n+1))
                QueueIO.addQueue("JobList","Excute",CatchListPath,"CatchList.py",CatchListQueue)
      
    except Exception as ex:
        LogHandler.writeDBMsg("Catch104",jsondata,ex)