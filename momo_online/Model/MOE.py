class MOEAAA():
    def __init__(self):
        self.TableName="MOEAAA"
        self.QueryStr="SELECT GUID, MOEAAA001, MOEAAA002, MOEAAA003, MOEAAA004, MOEAAA005, MOEAAA006, MOEAAA007, MOEAAA008, MOEAAA009, MOEAAA010, MOEAAA011, MOEAAA012, MOEAAA013, MOEAAA014, MOEAAA015, MOEAAA016, MOEAAA017, MOEAAA018, MOEAAA019, MOEAAA020, MOEAAA021, MOEAAA022, MOEAAA023, MOEAAA024, MOEAAA025, MOEAAA026, MOEAAA027, MOEAAA028, MOEAAA029, MOEAAA030, MOEAAA031, MOEAAA032, MOEAAA033, MOEAAA034, MOEAAA035, MOEAAA036, MOEAAA037, MOEAAA038, MOEAAA039, MOEAAA040, MOEAAA041, MOEAAA042, MOEAAA043, MOEAAA044, MOEAAA045, MOEAAA046, MOEAAA047, MOEAAA048, MOEAAA049, MOEAAA050, MOEAAA051, MOEAAA052, MOEAAA053, MOEAAA054, MOEAAA055, MOEAAA056, MOEAAA057, MOEAAA058, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM MOEAAA"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","MOEAAA001","MOEAAA002","MOEAAA003","MOEAAA004","MOEAAA005","MOEAAA006","MOEAAA007","MOEAAA008","MOEAAA009","MOEAAA010","MOEAAA011","MOEAAA012","MOEAAA013","MOEAAA014","MOEAAA015","MOEAAA016","MOEAAA017","MOEAAA018","MOEAAA019","MOEAAA020","MOEAAA021","MOEAAA022","MOEAAA023","MOEAAA024","MOEAAA025","MOEAAA026","MOEAAA027","MOEAAA028","MOEAAA029","MOEAAA030","MOEAAA031","MOEAAA032","MOEAAA033","MOEAAA034","MOEAAA035","MOEAAA036","MOEAAA037","MOEAAA038","MOEAAA039","MOEAAA040","MOEAAA041","MOEAAA042","MOEAAA043","MOEAAA044","MOEAAA045","MOEAAA046","MOEAAA047","MOEAAA048","MOEAAA049","MOEAAA050","MOEAAA051","MOEAAA052","MOEAAA053","MOEAAA054","MOEAAA055","MOEAAA056","MOEAAA057","MOEAAA058","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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

class MOEAAB():
    def __init__(self):
        self.TableName="MOEAAB"
        self.QueryStr="SELECT GUID, MOEAAB001, MOEAAB002, MOEAAB003, MOEAAB004, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM MOEAAB"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","MOEAAB001","MOEAAB002","MOEAAB003","MOEAAB004","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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

class MOEAAC():
    def __init__(self):
        self.TableName="MOEAAC"
        self.QueryStr="SELECT GUID, MOEAAC001, MOEAAC002, MOEAAC003, MOEAAC004, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM MOEAAC"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","MOEAAC001","MOEAAC002","MOEAAC003","MOEAAC004","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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

class MOEAAD():
    def __init__(self):
        self.TableName="MOEAAD"
        self.QueryStr="SELECT GUID, MOEAAD001, MOEAAD002, MOEAAD003, MOEAAD004, MOEAAD005, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM MOEAAD"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","MOEAAD001","MOEAAD002","MOEAAD003","MOEAAD004","MOEAAD005","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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

class MOEAAE():
    def __init__(self):
        self.TableName="MOEAAE"
        self.QueryStr="SELECT GUID, MOEAAE001, MOEAAE002, MOEAAE003, MOEAAE004, D_INSERTUSER, D_INSERTTIME, D_MODIFYUSER, D_MODIFYTIME FROM MOEAAE"
        self.KeyFields=["GUID"]
        self.Fields=["GUID","MOEAAE001","MOEAAE002","MOEAAE003","MOEAAE004","D_INSERTUSER","D_INSERTTIME","D_MODIFYUSER","D_MODIFYTIME"]
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