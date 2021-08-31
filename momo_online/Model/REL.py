class RELAAA():
    def __init__(self):
        self.TableName="RELAAA"
        self.QueryStr="SELECT GUID, RELAAA001, RELAAA002, RELAAA003, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM RELAAA"
        self.KeyFields=["RELAAA002"]
        self.Fields=["GUID","RELAAA001","RELAAA002","RELAAA003","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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