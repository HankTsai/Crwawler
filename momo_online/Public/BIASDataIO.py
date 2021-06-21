def findOption(dbcon,OptionName, OptionType):
    sql=("SELECT GUID FROM OPTAAA WHERE OPTAAA001=? AND OPTAAA003=?")
    OptionGUID= dbcon.GetDataTable(sql, (OptionName, OptionType))
    if OptionGUID is not None and len(OptionGUID)>0:
        return OptionGUID[0].GUID
    return ""

def insertOption(dbcon,OptionName, OptionCode, OptionType, RelGUID = None):
    import Public.PublicFun as PublicFun
    GUID=PublicFun.createID()
    sql=("INSERT INTO [dbo].[OPTAAA]([GUID],[OPTAAA001],[OPTAAA002],[OPTAAA003],[D_INSERTUSER],[D_INSERTTIME],[D_MODIFYUSER],[D_MODIFYTIME])"
    +"VALUES(?,?,?,?,'System',?,'','')")
    dbcon.Execute(sql, (GUID, OptionName, OptionCode, OptionType, PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS")))
    if RelGUID is not None:
        sql=("INSERT INTO [dbo].[OPTAAB]([GUID],[OPTAAB001],[OPTAAB002],[D_INSERTUSER],[D_INSERTTIME],[D_MODIFYUSER],[D_MODIFYTIME])"
        +"VALUES(?,?,?,'System',?,'','')")
        dbcon.Execute(sql, (PublicFun.createID(), RelGUID, GUID, PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS")))
    return GUID

def updateOption(dbcon, jobCategoryGuid, OptionCode):
    import Public.PublicFun as PublicFun
    sql=("UPDATE OPTAAA SET OPTAAA002=?, D_MODIFYTIME=? WHERE GUID = ?")
    dbcon.Execute(sql, (OptionCode, PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS"), jobCategoryGuid))

def findCompany(dbcon,CompanysName):
    sql=("SELECT GUID FROM Companys WHERE Companys003=?")
    CompanysGUID= dbcon.GetDataTable(sql, (CompanysName,))
    if CompanysGUID is not None and len(CompanysGUID)>0:
        return CompanysGUID[0].GUID
    return ""

def CheckMappingList(dbcon,MapType,Value):
    sql=("SELECT TOP 1 MAPAAA003 FROM MAPAAA WHERE MAPAAA001=? AND MAPAAA002=?")
    '''
    if ( MapType== "CompanyName"): 
    else:
        sql=("SELECT TOP 1 MAPAAA003 FROM MAPAAA WHERE MAPAAA001='"+MapType+"' AND MAPAAA002=N'"+Value+"'")
    '''
    return dbcon.GetDataTable(sql, (MapType, Value))

def insertMappingList(dbcon,MapType,Value,RelValue):
    import Public.PublicFun as PublicFun
    GUID=PublicFun.createID()
    sql=("INSERT INTO [dbo].[MAPAAA]([GUID],[MAPAAA001],[MAPAAA002],[MAPAAA003],[D_INSERTUSER],[D_INSERTTIME],[D_MODIFYUSER],[D_MODIFYTIME])"
    +"VALUES(?,?,?,?,'System',?,'','')")
    dbcon.Execute(sql, (GUID, MapType, Value, RelValue, PublicFun.getNowDateTime("YYYY/MM/DD HH:MM:SS")))
    return GUID

def CheckCompanyMappingList(dbcon,CompanyName,CompanyGUID=None,NewCompanyGUID=True):
    import Public.PublicFun as PublicFun
    MAPCompanyGUID = CheckMappingList(dbcon,"CompanyName",CompanyName)
    if MAPCompanyGUID is None or len(MAPCompanyGUID)==0:
        if CompanyGUID is None:
            CompanyGUID = findCompany(dbcon,CompanyName)
            if (CompanyGUID is None or CompanyGUID == ""):
                if (NewCompanyGUID):
                    CompanyGUID=PublicFun.createID()
                else:
                    CompanyGUID=""
        if (CompanyGUID != ""):
            insertMappingList(dbcon,"CompanyName",CompanyName,CompanyGUID)
    else:
        CompanyGUID=MAPCompanyGUID[0].MAPAAA003
    return CompanyGUID
