class field:
    def __init__(self):
        self.byteSize = None
        self.name = None
        self.abrv = None
        self.description = None
        self.mask = None
        self.size = None
        self.dataType = None
        self.baseType = None
    
    def setByteSize(self,byte):
        self.byteSize = byte

    def getByteSize(self):
        return self.byteSize

    def setBaseType(self,baseType):
        self.baseType = baseType

    def getBaseType(self):
        return self.baseType

    def setAbrv(self,abrv):
        self.abrv = abrv

    def getAbrv(self):
        return self.abrv

    def setName(self,name):
        self.name = name

    def setDescription(self,description):
        self.description = description

    def setMask(self,mask):
        self.mask = mask

    def setSize(self,size):
        self.size = size

    def setDataType(self,dataType):
        self.dataType = dataType

    def getName(self):
        return self.name
    
    def getDescription(self):
        return self.description
    
    def getMask(self):
        return self.mask

    def getSize(self):
        return self.size

    def getDataType(self):
        return self.dataType
