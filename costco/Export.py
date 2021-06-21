
import pyodbc

import pandas as pd
import zipcodetw


#取得日期格式By格式
def getNowDateTime(formatstr):
    import datetime
    formatstr = formatstr.upper()
    today = datetime.datetime.now()
    result = ""
    if (formatstr =="YYYY/MM/DD HH:MM:SS"):
        result = str(today.year).zfill(4) +"/"+str(today.month).zfill(2)+"/"+str(today.day).zfill(2)+" "+str(today.hour).zfill(2)+":"+str(today.minute).zfill(2)+":"+str(today.second).zfill(2)
    elif (formatstr =="YYYY/MM/DD"):
        result = str(today.year).zfill(4) +"/"+str(today.month).zfill(2)+"/"+str(today.day).zfill(2)
    elif (formatstr =="YYYY/MM"):
        result = str(today.year).zfill(4) +"/"+str(today.month-1).zfill(2)
    elif (formatstr =="HH:MM:SS"):
        result = str(today.hour).zfill(2)+":"+str(today.minute).zfill(2)+":"+str(today.second).zfill(2)
    return result



#幫忙補郵遞區號
def FillACPAAA016(df):
    #print(df["郵遞區號"])
    indexcol = int(df.columns.get_loc("郵遞區號")) 
    for index,row in df.iterrows():
        if (row.郵遞區號 == '' or row.郵遞區號 == None):
            df.iloc[index,indexcol] = str(zipcodetw.find(row.地址))
    return df




#幫忙補組織型態
def FillACPAAA021(df):
    indexcol = int(df.columns.get_loc("組織型態")) 
    for index,row in df.iterrows():
        if (row.組織型態 == '' or row.組織型態 == None):
            strtype="03 一般客戶"
            if(str(row.公司名稱).find("股份有限公司") >= 0 ):
                strtype = "0304 一般客戶-股份有限公司"
            elif(str(row.公司名稱).find("有限公司") >= 0 and str(row.公司名稱).find("股份") == -1 ):
                strtype = "0303 一般客戶-有限公司"
            elif(str(row.公司名稱).find("分公司") >= 0 ):
                strtype = "0305 一般客戶-分公司"
            df.iloc[index,indexcol] = str(strtype)
    return df


def get_sql():
    return ("select    "
            " CP.GUID   "
            " ,Companys003 公司名稱   "
            " ,Companys009 員工人數"
            " ,ACPAAA002 客戶代號      "
            " ,ISNULL(ACPAAA003,MOEAAA003)    客戶全名      "
            " ,ISNULL(ISNULL(ACPAAA004,MOEAAA029), Companys001)   統一編號  "
            " ,ACPAAA005    等級      "
            " ,ACPAAA006    職能別      "
            " ,ACPAAA007    公司網址      "
            " ,ACPAAA008    資本額區間      "
            " ,ACPAAA009    方案定位      "
            " ,ACPAAA010    行業大類      "
            " ,ACPAAA011    標靶分類"
            " ,ACPAAA012    公私田      "
            " ,ISNULL(ACPAAA013,MOEAAA009)    創立時間      "
            " ,ISNULL(ACPAAA014,MOEAAA006)    負責人      "
            " ,ISNULL(ISNULL(ISNULL(ACPAAA015,MOEAAA007), Companys005), '')    地址      "
            " ,ACPAAA016    郵遞區號      "
            " ,ISNULL(ACPAAA017,MOEAAA004)    資本額      "
            " ,ACPAAA018    產業別      "
            " ,ACPAAA019    行業別      "
            " ,ACPAAA020    地區別      "
            " ,ACPAAA021    組織型態      "
            " ,ACPAAA022    工廠證號      "
            " ,ACPAAA023    主要產品      "
            " ,ACPAAA024    最近修改日      "
            " ,ACPAAA025    最近修改人      "
            " ,ACPAAA026    聯絡人      "
            " ,ACPAAA027    部門名稱      "
            " ,ACPAAA028    職稱      "
            " ,ACPAAA029    電話      "
            " ,ACPAAA030    行動電話_1    "  
            " ,ACPAAA031    傳真      "
            " ,ACPAAA032    EMAIL      "
            " ,ACPAAA033    軟體使用來源      "
            " ,ACPAAA034    舊客等級      "
            " ,ACPAAA035    EMAIL2    " 
            " ,ACPAAA036    購買產品      "
            " ,ACPAAA037    行業分流      "
            " ,ACPAAA038    銷售等級      "
            " ,ACPAAA039    責任部門      "
            " ,ACPAAA040    責任規劃師      "
            " ,ACPAAA041    日報建立者      "
            " ,ACPAAA042    聯繫日期      "
            " ,ACPAAA043    日報聯絡人      "
            " ,ACPAAA044    日報工作內容      "
            " ,ACPAAA045    事業單位日報建立者      "
            " ,ACPAAA046    事業單位日報聯繫日期      "
            " ,ACPAAA047    事業位日報工作內容      "
            " ,ACPAAA048    五碼分流      "
            " ,ACPAAA049    標靶      "
            " ,ACPAAA050    上市櫃別     "
            " ,ACPAAA051   行業名稱      "
            " ,ACPAAA052    兩碼行業代號      "
            " ,ACPAAA053    兩碼行業名稱    "
            " FROM Companys CP  "
            " LEFT JOIN ACPAAA AA on AA.ACPAAA002 = CP.Companys002  "
            " LEFT JOIN MOEAAA MOA on MOA.MOEAAA001 = CP.GUID  "
            " WHERE CP.GUID IN (select distinct CompanyProduct001 from CompanyProduct)"
            " ORDER BY ACPAAA002")
    
def main() : 
    #,autocommit=False
    cnxn = pyodbc.connect("DRIVER={SQL Server};SERVER=10.20.81.24;DATABASE=WebFormPT_BIAS;UID=varysdb;PWD=DigiWin_#@!")
    writer = pd.ExcelWriter('export\Costco'+getNowDateTime("YYYY/MM/DD").replace('/','')+'.xlsx', engine='xlsxwriter',  options={'strings_to_urls': False})
    #更新VIEW
    df = pd.read_sql(sql=get_sql() , con=cnxn)
    df=FillACPAAA016(df)
    df=FillACPAAA021(df)
    df.drop(df.columns[[0]], axis=1, inplace=True)
    df.to_excel(writer,sheet_name="Costco")
    writer.save()
    cnxn.close()

#主要執行邏輯
if __name__ == "__main__":
    main()
