import sys
from bs4 import BeautifulSoup as bs


import Public.PublicFun as PublicFun
import Public.RequestsHandler as RequestsHandler
import Public.SettingReader as SettingReader
import Public.QueueIO as QueueIO
import Public.LogHandler as LogHandler
import Public.SQLConnect as SQLConnect
import Public.Engine as Engine

import Model.JOB as JOB

if __name__ == '__main__':
    jsondata=""
    try:
        JobID=sys.argv[1]
        data=sys.argv[2]
        jsondata = PublicFun.StringToJson(data)
        CompanyGUID=str(jsondata["CompanyGUID"])
        JOBAAA009=str(jsondata["JOBAAA009"])

        requestHost=SettingReader.getSetting("global","requestHost")
        
        DBConnect=SQLConnect.DBConnect(publicSetting=True)
        DBConnect.ConnectDB()
        
#        sql = "select GUID,JOBAAA009 from JOBAAA with(nolock) where JOBAAA029 != 'Y'"
#        dt = DBConnect.GetDataTable(sql)
        if(len(JOBAAA009) >0):
            req=RequestsHandler.getNewRequests(str(JOBAAA009),requestHost)
#            for rows in dt:
            if (len(str(JOBAAA009)) > 0 ):
                res = req.get(str(JOBAAA009))
                if (res.text.find("你要找的工作或公司已結束徵才") > 0):
                    objJob=Engine.Query(DBConnect,JOB.JOBAAA(),"GUID='"+str(CompanyGUID)+"'")
                    objJob.D_MODIFYUSER="UpdateJobEndRecruit"
                    objJob.JOBAAA029 ="Y"
                    Engine.UpdateData(DBConnect,objJob)
                    
        DBConnect.close() 
    except Exception as ex:
        print("母體請重置此Queue")
        LogHandler.writeDBMsg("UpdateJobEndRecruit",jsondata,ex)