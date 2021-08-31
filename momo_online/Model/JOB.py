class JOBAAA():
    def __init__(self):
        self.TableName="JOBAAA"
        self.QueryStr="SELECT GUID, JOBAAA001, JOBAAA002, JOBAAA003, JOBAAA004, JOBAAA005, JOBAAA006, JOBAAA007, JOBAAA008, JOBAAA009, JOBAAA010, JOBAAA011, JOBAAA012, JOBAAA013, JOBAAA014, JOBAAA015, JOBAAA016, JOBAAA017, JOBAAA018, JOBAAA019, JOBAAA020, JOBAAA021, JOBAAA022, JOBAAA023, JOBAAA024, JOBAAA025, JOBAAA026, JOBAAA027, JOBAAA028, JOBAAA029, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM JOBAAA"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","JOBAAA001","JOBAAA002","JOBAAA003","JOBAAA004","JOBAAA005","JOBAAA006","JOBAAA007","JOBAAA008","JOBAAA009","JOBAAA010","JOBAAA011","JOBAAA012","JOBAAA013","JOBAAA014","JOBAAA015","JOBAAA016","JOBAAA017","JOBAAA018","JOBAAA019","JOBAAA020","JOBAAA021","JOBAAA022","JOBAAA023","JOBAAA024","JOBAAA025","JOBAAA026","JOBAAA027","JOBAAA028","JOBAAA029","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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

class JOBAAB():
    def __init__(self):
        self.TableName="JOBAAB"
        self.QueryStr="SELECT GUID, JOBAAB001, JOBAAB002, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM JOBAAB"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","JOBAAB001","JOBAAB002","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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
