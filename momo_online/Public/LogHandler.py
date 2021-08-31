import Public.PublicFun as PublicFun
import Public.SQLConnect as SQLConnect
import json

def writeMsg(msg):
    import time 
    msg=str(time.strftime('%Y%m%d%H%M%S'))+":"+msg+"\n"
    print(msg, end='')

def writethreadMsg(threadCount,msg):
    writeMsg("執行續"+str(threadCount)+" "+msg)
    
def writeDBMsg(JobName,Param,msg,dbcon=None):
    jsonData = Param
    if type(jsonData) is not str :
        jsonData = json.dumps(Param, separators=(',', ':'))
    
    if dbcon is None:
        dbcon=SQLConnect.DBConnect(secName="QueueConnect", publicSetting=True)
        dbcon.ConnectDB()
        writeDBMsg(JobName,jsonData,msg,dbcon)
        dbcon.close()
    else:
        try:
            sql=("INSERT INTO [dbo].[LogMsg]([GUID],[JOB],[Param],[Message],[D_INSERTUSER],[D_INSERTTIME],[D_MODIFYUSER],[D_MODIFYTIME])"
            +"VALUES(?, ?, ?, ?, ?, ?, ?, ?)")
            dbcon.Execute(sql, (PublicFun.createID(), JobName, jsonData, msg, JobName, PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS"), "", ""))
            writeMsg(str(msg))
        except Exception as ex:
            writeMsg("寫入資料庫失敗:"+ex)
    