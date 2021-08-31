class TRAAAA():
    def __init__(self):
        self.TableName="TRAAAA"
        self.QueryStr="SELECT GUID, TRAAAA001, TRAAAA002, TRAAAA003, TRAAAA004, TRAAAA005, TRAAAA006, TRAAAA007, TRAAAA008, TRAAAA009, TRAAAA010, TRAAAA011, TRAAAA012, TRAAAA013, TRAAAA014, TRAAAA015, TRAAAA016, TRAAAA017, TRAAAA018, TRAAAA019, TRAAAA020, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM TRAAAA"
        self.KeyFields=["TRAAAA001"]
        self.Fields=["GUID","TRAAAA001","TRAAAA002","TRAAAA003","TRAAAA004","TRAAAA005","TRAAAA006","TRAAAA007","TRAAAA008","TRAAAA009","TRAAAA010","TRAAAA011","TRAAAA012","TRAAAA013","TRAAAA014","TRAAAA015","TRAAAA016","TRAAAA017","TRAAAA018","TRAAAA019","TRAAAA020","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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