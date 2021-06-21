class Companys():
    def __init__(self):
        self.TableName="Companys"
        self.QueryStr="SELECT GUID, Companys001, Companys002, Companys003, Companys004, Companys005, Companys006, Companys007, Companys008, Companys009, Companys010, Companys011, Companys012,Companys013, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM Companys"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","Companys001","Companys002","Companys003","Companys004","Companys005","Companys006","Companys007","Companys008","Companys009","Companys010","Companys011","Companys012","Companys013","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
        self.CheckTimeStamp=True
        self.DataRow=[]
        self.TimeStamp=""
    
    def __getattr__(self, Column):
        return self.DataRow[self.Fields.index(Column)]

    def getData(self,Column):
        if Column in self.__dict__:
            return self.__dict__[Column]
        else:
            return self.__getattr__(Column)

class CompanyIntro():
    def __init__(self):
        self.TableName="CompanyIntro"
        self.QueryStr="SELECT GUID, CompanyIntro001, CompanyIntro002, CompanyIntro003, CompanyIntro004, CompanyIntro005, CompanyIntro006, CompanyIntro007, CompanyIntro008, CompanyIntro009, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM CompanyIntro"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","CompanyIntro001","CompanyIntro002","CompanyIntro003","CompanyIntro004","CompanyIntro005","CompanyIntro006","CompanyIntro007","CompanyIntro008","CompanyIntro009","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
        self.CheckTimeStamp=True
        self.DataRow=[]
        self.TimeStamp=""
    
    def __getattr__(self, Column):
        return self.DataRow[self.Fields.index(Column)]

    def getData(self,Column):
        if Column in self.__dict__:
            return self.__dict__[Column]
        else:
            return self.__getattr__(Column)