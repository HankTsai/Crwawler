import sys
from bs4 import BeautifulSoup as bs
import datetime
import requests
import json

import Public.PublicFun as PublicFun
import Public.SettingReader as SettingReader
import Public.SQLConnect as SQLConnect
import Public.QueueIO as QueueIO

if __name__ == '__main__':
    try:
        JobID=sys.argv[1]
        data=sys.argv[2]
        jsondata = PublicFun.StringToJson(data)
        
        DBConnect=SQLConnect.DBConnect(publicSetting=True)
        DBConnect.ConnectDB()
        sql=""
        if "Update" in jsondata:
            sql=("select GUID,JOBAAA009 from JOBAAA with(nolock) where JOBAAA029 != 'Y'")
        elif "Insert" in jsondata:
            sql=("select GUID,JOBAAA009 from JOBAAA with(nolock) where JOBAAA029 != 'Y'")
        else:
            raise Exception("無動作指令")
        
        CatchListPath=SettingReader.getSetting("excutePath","CatchList")
        
        rows = DBConnect.GetDataTable(sql)
        
        for row in rows:
            tmpQueue=QueueIO.setParameter("CompanyGUID",row.GUID)
            tmpQueue=QueueIO.setParameter("JOBAAA009",row.JOBAAA009,tmpQueue)
            QueueIO.addQueue("UpdateJobEndRecruit","Excute",CatchListPath,"UpdateJobEndRecruit.py",tmpQueue)
        DBConnect.close()
    except Exception as ex:
        print(ex)