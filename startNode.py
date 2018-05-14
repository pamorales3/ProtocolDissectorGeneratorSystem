from node import *
class startNode:
    def __init__(self):
        self.node = node("start") #will contain the connector also
        self.protocolName = None
        self.protocolDescription = None
        self.dependentProtocolName = None
        self.dependencyPattern = None

    def setProtocolName(self,name):
        self.protocolName = name

    def searchNode(self,name):
        return self.node.searchNode(name)

    def setProtocolDescription(self,description):
        self.protocolDescription = description

    def setDependentProtocolName(self,name):
        self.dependentProtocolName = name

    def setDependencyPattern(self,pattern):
        self.dependencyPatter = pattern

    def getStartNode(self):
        return self.node

    def addNode(self,node):
        self.node.addNode(node)#addNewNode
    def addDecisionNode(self,true,false):
        self.node.addDecisionNode(true,false)
        
    
    
