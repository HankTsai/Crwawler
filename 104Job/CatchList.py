import sys
from bs4 import BeautifulSoup as bs


import Public.PublicFun as PublicFun
import Public.RequestsHandler as RequestsHandler
import Public.SettingReader as SettingReader
import Public.QueueIO as QueueIO
import Public.LogHandler as LogHandler

def getDataDate(StandardDate):
    import datetime
    today = datetime.datetime.now()
    ScanDate=today+datetime.timedelta(days=StandardDate)
    result = str(ScanDate.year).zfill(4) +"/"+str(ScanDate.month).zfill(2)+"/"+str(ScanDate.day).zfill(2)
    return result

if __name__ == '__main__':
    jsondata=""
    try:
        JobID=sys.argv[1]
        data=sys.argv[2]
        jsondata = PublicFun.StringToJson(data)
        ListURL=str(jsondata["URL"])
        
        CatchCompanyPath=SettingReader.getSetting("excutePath","CatchCompany")
        CatchJobPath=SettingReader.getSetting("excutePath","CatchJob")
        DateStandard=int(SettingReader.getSetting("global","DateStandard"))

        requestHost=SettingReader.getSetting("global","requestHost")
        req=RequestsHandler.getNewRequests(ListURL,requestHost)
        res = req.get(ListURL)
        res.encoding = 'utf8'
        Soup = bs(res.text, "html.parser")
        JobContent=Soup.find("div",id="js-job-content")
        if JobContent is not None:
            JobContent=JobContent.select("article.js-job-item ul")
            ScanDate = getDataDate(DateStandard)

            for tempContent in JobContent:
                if tempContent.attrs is not None and len(tempContent.attrs)>0:
                    continue
                
                if len(tempContent.select('li.job-mode__date'))>0:
                    checkDate=tempContent.select('li.job-mode__date')[0].text.replace('\n','').replace(' ','')
                    if checkDate != "":
                        checkDate=checkDate.split("/")[0].zfill(2)+"/"+checkDate.split("/")[1].zfill(2)
                        if checkDate !=ScanDate[5:]:
                            continue

                #region 公司
                tempcompany=tempContent.select('li.job-mode__company a')[0]
                tempurl="https:"+tempcompany["href"]
                CompanyQueue=QueueIO.setParameter("companyName",tempcompany.text)
                CompanyQueue=QueueIO.setParameter("companyURL",tempurl,CompanyQueue)
                QueueIO.addQueue("104Company","Excute",CatchCompanyPath,"CatchCompany.py",CompanyQueue)
                #endregion

                #region 職缺
                #日期
                tempDate=""
                if len(tempContent.select('li.job-mode__date'))>0:
                    tempDate=tempContent.select('li.job-mode__date')[0].text.replace('\n','').replace(' ','')
                JobQueue=QueueIO.setParameter("date",tempDate)
                if (tempDate == ""):
                        continue
                #職務
                tempJob=tempContent.select('li.job-mode__jobname a')[0]
                JobQueue=QueueIO.setParameter("jobName",tempJob.text,JobQueue)
                tempurl="https:"+tempJob["href"]
                JobQueue=QueueIO.setParameter("jobURL",tempurl,JobQueue)
                if (tempurl == "https:javascript:void(0);"):
                        continue
                #地區
                JobQueue=QueueIO.setParameter("jobAREA",tempContent.select('li.job-mode__area')[0].text,JobQueue)

                #公司
                JobQueue=QueueIO.setParameter("companyInfo",CompanyQueue,JobQueue)

                #日期基準
                JobQueue=QueueIO.setParameter("ScanDate",ScanDate,JobQueue)
        
                QueueIO.addQueue("104Job","Excute",CatchJobPath,"CatchJob.py",JobQueue)
                #endregion
                
    except Exception as ex:
        print("母體請重置此Queue")
        LogHandler.writeDBMsg("Catch104",jsondata,ex)