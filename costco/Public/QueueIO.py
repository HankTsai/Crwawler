class QueueJob():
    def __init__(self):
        self.SystemName = ""
        self.QueueType =""
        self.Path = ""
        self.Files = ""
        self.Param = None
        self.Guid = ""
        
def delJob(guid) :
    dbcon=getQueueDBConnect()
    sql="delete FROM JobQueue WHERE GUID=?"
    dbcon.Execute(sql, (guid,))
    dbcon.close()

def getQueue(SystemName,QueueType):
    #from queue import Queue
    #resultQueue=Queue()
    resultQueue = []
    sql=(
        "SELECT * FROM JobQueue WHERE SystemName=? AND QueueType=? order by D_INSERTTIME" 
    )
    dbcon=getQueueDBConnect()
    dt=dbcon.GetDataTable(sql, (SystemName, QueueType))
    for row in dt:
        tmpJob=QueueJob()
        tmpJob.Guid=row.GUID
        tmpJob.SystemName=row.SystemName
        tmpJob.QueueType=row.QueueType
        tmpJob.Path=row.Path
        tmpJob.Files=row.Files
        tmpJob.Param=row.Param
        #resultQueue.put(tmpJob)
        resultQueue.append(tmpJob)
        '''
        sql=(
            "delete FROM JobQueue WHERE GUID=?" 
        )
        dbcon.Execute(sql, (row.GUID))
        '''

    dbcon.close()
    return resultQueue

def addQueueJob(QueueJobObj):
    addQueue(QueueJobObj.SystemName,QueueJobObj.QueueType,QueueJobObj.Path,QueueJobObj.Files,QueueJobObj.Param)

def addQueue(SystemName,QueueType,Path,Files,Param):
    import Public.PublicFun as PublicFun
    import json
    GUID=PublicFun.createID()
    #str(Param)
    jsonData = Param
    if type(Param) is not str :
        jsonData = json.dumps(Param, separators=(',', ':'))
    dbcon=getQueueDBConnect()
    if checkQueue(SystemName, QueueType, jsonData, dbcon) :
        retry = 0
        while True :
            try :
                if retry > 10 :
                    break
                else :
                    D_INSERTTIME = PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS")
                    sql=(
                        "INSERT INTO [dbo].[JobQueue]([GUID],[SystemName],[QueueType],[Path],[Files],[Param],[D_INSERTTIME])"+
                        "VALUES(?,?,?,?,?,?,?)"
                    )
                    dbcon.Execute(sql, (GUID, SystemName, QueueType, Path, Files, jsonData, D_INSERTTIME))
                    break
            except Exception as ex:
                #若是寫入失敗, 則重試, 最多試10次
                retry += 1
                print("Retry:" + str(retry))
    dbcon.close()
    
#檢查是否已有相同的資料
def checkQueue(SystemName, QueueType, Param, dbcon) :
    sql=(
        "SELECT GUID FROM JobQueue WHERE SystemName=? AND QueueType=? AND [Param]=? order by D_INSERTTIME" 
    )
    #dbcon=getQueueDBConnect()
    dt=dbcon.GetDataTable(sql, (SystemName, QueueType, Param))
    #dbcon.close()
    if len(dt) > 0 :
        return False
    else :
        return True


def setParameter(Key,Value,JsonObj=None):
    import json
    if JsonObj is None:
        JsonObj=json.loads("{}")
    if Key in JsonObj:
        raise Exception("Key重複")
    JsonObj[Key]=Value
    return JsonObj

def writeDBMsg(msg):
    import Public.PublicFun as PublicFun
    import Public.LogHandler as LogHandler
    
    dbcon=getQueueDBConnect()
    sql=(
    "INSERT INTO [dbo].[LogMsg]([GUID],[Message],[D_INSERTTIME])"+
    "VALUES(?,?,?)"
    )
    try:
        dbcon.Execute(sql, (PublicFun.createID(), PublicFun.SQLFilter(msg), PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS")))
    except:
        msg="writeDBMsg失敗："+msg
    LogHandler.writeMsg(msg)
    dbcon.close()

def getQueueDBConnect():
    import Public.SQLConnect as SQLConnect
    DBConnect=SQLConnect.DBConnect("QueueConnect",publicSetting=True)
    DBConnect.ConnectDB()
    return DBConnect
    