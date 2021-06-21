import sys
from bs4 import BeautifulSoup as bs
import datetime
from functools import reduce

import Public.PublicFun as PublicFun
import Public.BIASDataIO as BIASDataIO
import Public.SQLConnect as SQLConnect
import Public.SettingReader as SettingReader
import Public.RequestsHandler as RequestsHandler
import Public.Engine as Engine
import Public.LogHandler as LogHandler

import Model.JOB as JOB

def getPhoneNumber(PhoneNumberurl):
    #Regex格式驗證
    import re
    text_re=re.compile('Text=')
    queryString= PhoneNumberurl.split("&")
    for param in queryString:
        if len(text_re.findall(param))>0:
            return param[5:]

if __name__ == '__main__':
    jsondata=""
    try:
        JobID=sys.argv[1]
        data=sys.argv[2]
        
        jsondata = PublicFun.StringToJson(data)
        jobdate=str(jsondata["date"])
        jobName=PublicFun.SQLFilter(str(jsondata["jobName"]))
        jobURL=str(jsondata["jobURL"])
        jobAREA=str(jsondata["jobAREA"])
        companyInfo=jsondata["companyInfo"]
        try:
            companyName=PublicFun.SQLFilter(str(companyInfo["companyName"]))
        except Exception as ex:
            companyInfo = PublicFun.StringToJson(companyInfo,Default=False)
            companyName=PublicFun.SQLFilter(str(companyInfo["companyName"]))
        ScanDate=str(jsondata["ScanDate"])

        DBConnect=SQLConnect.DBConnect(publicSetting=True)
        DBConnect.ConnectDB()

        CompanyGUID=BIASDataIO.CheckCompanyMappingList(DBConnect,companyName)
        requestHost=SettingReader.getSetting("global","requestHost")
        req=RequestsHandler.getNewRequests(jobURL,requestHost)
        res=req.get(jobURL)
        res.encoding = 'utf8'
        JobSoup = bs(res.text, "html.parser")    
        objJob=Engine.Query(DBConnect,JOB.JOBAAA(),"JOBAAA009 = '"+jobURL.strip()+"'")
        if (objJob.GUID ==""):
            objJob.GUID=PublicFun.createID()
            objJob.D_INSERTUSER="CatchJob"
        else:
            objJob.D_MODIFYUSER="CatchJob"
        objJob.JOBAAA001=CompanyGUID
        objJob.JOBAAA002="104"
        objJob.JOBAAA003=jobName.strip()
        objJob.JOBAAA005=jobAREA.strip()
        objJob.JOBAAA009=jobURL.strip()
        contentInfo=JobSoup.find("dt", text="聯絡人：")
        if contentInfo is not None :
            objJob.JOBAAA006=contentInfo.find_next_sibling("dd").text.strip()
        contentInfo=JobSoup.find("dt", text="電洽：")
        if contentInfo is not None :
            contentInfo=contentInfo.find_next_sibling("dd").find("img")["src"]
            objJob.JOBAAA008=getPhoneNumber(contentInfo).strip()
        contentInfo=JobSoup.find("dt", text="E-mail：")
        if contentInfo is not None :
            objJob.JOBAAA007=contentInfo.find_next_sibling("dd").text.strip()
        
        contentInfo=JobSoup.find("h2", text="工作內容")
        if contentInfo is not None :
            contentInfo=contentInfo.find_next_sibling("div").select("p")
            if len(contentInfo)>0:
                objJob.JOBAAA010=contentInfo[0].text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="工作待遇：")
        if contentInfo is not None :
            objJob.JOBAAA011=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="工作性質：")
        if contentInfo is not None :
            objJob.JOBAAA012=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="上班地點：")
        if contentInfo is not None :
            objJob.JOBAAA013=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="管理責任：")
        if contentInfo is not None :
            objJob.JOBAAA014=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="出差外派：")
        if contentInfo is not None :
            objJob.JOBAAA015=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="上班時段：")
        if contentInfo is not None :
            objJob.JOBAAA016=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="休假制度：")
        if contentInfo is not None :
            objJob.JOBAAA017=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="可上班日：")
        if contentInfo is not None :
            objJob.JOBAAA018=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="需求人數：")
        if contentInfo is not None :
            objJob.JOBAAA019=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="接受身份：")
        if contentInfo is not None :
            objJob.JOBAAA020=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="工作經歷：")
        if contentInfo is not None :
            objJob.JOBAAA021=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="學歷要求：")
        if contentInfo is not None :
            objJob.JOBAAA022=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="科系要求：")
        if contentInfo is not None :
            objJob.JOBAAA023=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="語文條件：")
        if contentInfo is not None :
            objJob.JOBAAA024=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="擅長工具：")
        if contentInfo is not None :
            objJob.JOBAAA025=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="工作技能：")
        if contentInfo is not None :
            objJob.JOBAAA026=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("dt", text="其他條件：")
        if contentInfo is not None :
            objJob.JOBAAA027=contentInfo.find_next_sibling("dd").text.replace('\n','').replace('\r','').strip()

        contentInfo=JobSoup.find("h2", text="公司福利")
        if contentInfo is not None :
            objJob.JOBAAA028=contentInfo.find_next_sibling("div").text.replace('\n','').replace('\r','').strip()
        contentInfo=JobSoup.select("time")
        if len(contentInfo)>0:
            jobdate=contentInfo[0].text[5:]
            jobdate=jobdate.replace("-","/")
        elif jobdate is not None and jobdate != "":
            jobdatespl=jobdate.split("/")
            jobdate=str(datetime.datetime.now().year).zfill(4)+"/"+str(jobdatespl[0]).zfill(2)+"/"+str(jobdatespl[1]).zfill(2)
        objJob.JOBAAA004=jobdate.strip()
        
        #if jobdate==ScanDate:
        Engine.UpdateData(DBConnect,objJob)

        CategoryList=JobSoup.select("dd.cate span")
        for category in CategoryList:
            if category.text=="":
                continue
            objCategory=Engine.Query(DBConnect,JOB.JOBAAB(),"1=2")
            categoryGUID=BIASDataIO.findOption(DBConnect,category.text.replace('／','╱'))
            objCategory.GUID=PublicFun.createID()
            objCategory.D_INSERTUSER="CatchJob"
            objCategory.JOBAAB001=objJob.GUID
            objCategory.JOBAAB002=categoryGUID
            Engine.UpdateData(DBConnect,objCategory)
        DBConnect.close()
    except Exception as ex:
        print("母體請重置此Queue")
        LogHandler.writeDBMsg("CatchJob",jsondata,ex)