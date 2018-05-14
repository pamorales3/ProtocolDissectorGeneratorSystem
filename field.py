class field:
    def __init__(self):
        self.name = None
        self.description = None
        self.mask = None
        self.size = None
        self.dataType = None

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
