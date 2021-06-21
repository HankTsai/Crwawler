import sys
from bs4 import BeautifulSoup as bs
import datetime

import Public.PublicFun as PublicFun
import Public.BIASDataIO as BIASDataIO
import Public.SQLConnect as SQLConnect
import Public.SettingReader as SettingReader
import Public.RequestsHandler as RequestsHandler
import Public.NumberTransform as NumberTransform
import Public.QueueIO as QueueIO
import Public.Engine as Engine
import Public.LogHandler as LogHandler

import Model.Companys as Companys

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
        companyURL=str(jsondata["companyURL"])
        companyName=str(jsondata["companyName"])

        DBConnect=SQLConnect.DBConnect(publicSetting=True)
        DBConnect.ConnectDB()

        CompanyGUID=BIASDataIO.CheckCompanyMappingList(DBConnect,companyName)
        companyInFo=Engine.Query(DBConnect,Companys.Companys(),"GUID='"+CompanyGUID+"'")

        if companyInFo.GUID =="":
            companyInFo.GUID=CompanyGUID
            companyInFo.D_INSERTUSER="CatchCompany"
        else:
            companyInFo.D_MODIFYUSER="CatchCompany"

        today=PublicFun.getNowDateTime("YYYY/MM/DD")
        if companyInFo.D_INSERTTIME is None or (companyInFo.D_MODIFYTIME =="" and companyInFo.D_INSERTTIME[:10]<today) or (companyInFo.D_MODIFYTIME !="" and companyInFo.D_MODIFYTIME[:10]<today):
            companyIntro=Engine.Query(DBConnect,Companys.CompanyIntro(),"CompanyIntro001='"+CompanyGUID+"'")                        
            if companyIntro.GUID is None or companyIntro.GUID =="":
                companyIntro.GUID=PublicFun.createID()
                companyIntro.D_INSERTUSER="CatchCompany"
            else:
                companyIntro.D_MODIFYUSER="CatchCompany"
            companyIntro.CompanyIntro001=CompanyGUID
            companyInFo.Companys003=companyName

            requestHost=SettingReader.getSetting("global","requestHost")
            req=RequestsHandler.getNewRequests(companyURL,requestHost)
            res=req.get(companyURL)
            res.encoding = 'utf8'
            CompanySoup = bs(res.text, "html.parser")    

            contentInfo=CompanySoup.select("div.intro dl")
            contentInfo=contentInfo[0].text.splitlines()
            for n in range(len(contentInfo)):
                colname=contentInfo[n].replace(u"\xa0","").replace("　","")
                if colname=="產業類別：":
                    companyIntro.CompanyIntro002=contentInfo[n+1]
                    n=n+1
                if colname=="產業描述：":
                    companyIntro.CompanyIntro003=contentInfo[n+1]
                    n=n+1
                if colname=="員工：":
                    companyInFo.Companys009=NumberTransform.transformNumber(contentInfo[n+1])
                    n=n+1
                if colname=="資本額：":
                    companyInFo.Companys007=NumberTransform.transformNumber(contentInfo[n+1])
                    n=n+1
                if colname=="聯絡人：":
                    companyIntro.CompanyIntro004=contentInfo[n+1]
                    n=n+1
                if colname=="電話：":
                    try:
                        Phone=getPhoneNumber(CompanySoup.find("dt",text=contentInfo[n]).find_next_sibling("dd").find("img")["src"])
                    except:
                        Phone=""
                    Phone=Phone+contentInfo[n+1]
                    companyInFo.Companys010=Phone
                    companyIntro.CompanyIntro005=Phone
                    n=n+1
                if colname=="傳真：":
                    try:
                        Fax=getPhoneNumber(CompanySoup.find("dt",text=contentInfo[n]).find_next_sibling("dd").find("img")["src"])
                    except:
                        Fax=""
                    companyInFo.Companys011=Fax+contentInfo[n+1]
                    n=n+1
                if colname=="公司網址：":
                    companyInFo.Companys012=contentInfo[n+1]
                    n=n+1
            contentInfo=CompanySoup.find("dt", text="公司地址：")
            if contentInfo is not None :
                Locate=contentInfo.find_next_sibling("dd").text
                companyInFo.Companys005=Locate.rstrip('\n').rstrip("地圖")

            CompanyIntroSoup=CompanySoup.find("div",id="intro")
            contentInfo=CompanyIntroSoup.find("h2",text="公司簡介")
            if contentInfo is not None :
                companyIntro.CompanyIntro006=contentInfo.find_next_sibling("p").text.replace("\r","\r\n")

            contentInfo=CompanyIntroSoup.find("h2",text="主要商品／服務項目")
            if contentInfo is not None :
                companyIntro.CompanyIntro007=contentInfo.find_next_sibling("p").text.replace("\r","\r\n")
            
            contentInfo=CompanyIntroSoup.find("h2",text="福利制度")
            if contentInfo is not None :
                companyIntro.CompanyIntro008=contentInfo.find_next_sibling("p").text.replace("\r","\r\n")

            contentInfo=CompanyIntroSoup.find("h2",text="經營理念")
            if contentInfo is not None :
                companyIntro.CompanyIntro009=contentInfo.find_next_sibling("p").text.replace("\r","\r\n")
            
            companyInFo.Companys013 = companyURL

            Engine.UpdateData(DBConnect,companyInFo)
            Engine.UpdateData(DBConnect,companyIntro)
            
        DBConnect.close()  
    except Exception as ex:
        print("母體請重置此Queue")
        LogHandler.writeDBMsg("CatchCompany",jsondata,ex)