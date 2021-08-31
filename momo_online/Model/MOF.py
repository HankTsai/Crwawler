class MOFAAA():
    def __init__(self):
        self.TableName="MOFAAA"
        self.QueryStr="SELECT GUID, MOFAAA001, MOFAAA002, MOFAAA003, MOFAAA004, MOFAAA005, MOFAAA006, MOFAAA007, MOFAAA008, MOFAAA009, MOFAAA010, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM MOFAAA"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","MOFAAA001","MOFAAA002","MOFAAA003","MOFAAA004","MOFAAA005","MOFAAA006","MOFAAA007","MOFAAA008","MOFAAA009","MOFAAA010","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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

class MOFAAB():
    def __init__(self):
        self.TableName="MOFAAB"
        self.QueryStr="SELECT GUID, MOFAAB001, MOFAAB002, MOFAAB003, MOFAAB004, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM MOFAAB"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","MOFAAB001","MOFAAB002","MOFAAB003","MOFAAB004","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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
