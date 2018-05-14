from startNode import *
from endNode import *
from node import *
from os import *
import xml.etree.ElementTree as et

class protocolDecisionTreeConstruct:
    def __init__(self):
        self.startNode = startNode()
        self.endNode = endNode()
        self.startNode.addNode(self.endNode)

    def getXMl(self):
        root = et.Element("root")
        self.startNode.node.createXML(root,0)
        tree = et.ElementTree(root)
        tree.write("file.xml")

    
    def createList(self):
        return self.startNode.node.createList()
    
    def setOperand(self,name,operand):
        insert = self.startNode.searchNode(name)
        insert.expression.setOperand(operand)
    
    def getOperand(self,name):
        insert = self.startNode.searchNode(name)
        return insert.expression.getOperand()
    
    def setRelationalOperator(self,name,operator):#name of node
        insert = self.startNode.searchNode(name)
        insert.expression.setRelationalOperator(operator)
    
    def setLogicalOperator(self,name,operator):
        insert = self.startNode.searchNode(name)
        insert.expression.setLogicalOperator(operator)
    
    def getRelationalOperator(self,name):
        insert = self.startNode.searchNode(name)
        return insert.expression.getRelationalOperator()
    
    def getLogicalOperator(self,name):
        insert = self.startNode.searchNode(name)
        return insert.expression.getLogicalOperator()
    
    def addNewNode(self,node,name):#name of node
        insert = self.startNode.searchNode(name)
        insert.addNode(node)
    
    def addDecisionNode(self,true,false,name):
        insert = self.startNode.searchNode(name)
        insert.addDecisionNode(true,false)
    
    def setEndNode(self,endNode):
        if isinstance(endNode,endNode):
            self.endNode = endNode
        else:
            print "not endNode"
    
    def setStartNode(self,protocolName,protocolDescription,dependentProtocolName,dependencyPattern):
        start = startNode()
        start.setProtocolName(protocolName)
        start.setProtocolDescription(protocolDescription)
        start.setDependentProtocolName(dependentProtocolName)
        start.setDependencyPattern(dependencyPattern)
        next = self.startNode.node.nextNode
        start.node.nextNode = next
        self.startNode = start

    def createNode(self,name):
        newNode = node(name)
        return newNode
    
    def getStartNode(self):
        return startNode
        
    def getFieldInfo(self,byte,name,abrv,description,mask,size,dataType,baseType):
        node = self.startNode.searchNode(name)
        if name == True:
            return node.field.getName()
        elif byte == True:
            return node.field.getByteSize()
        elif abrv == True:
            return node.field.getAbrv()
        elif description == True:
            return node.field.getDescription()
        elif mask == True:
            return node.field.getMask()
        elif size == True:
            return node.field.getSize()
        elif dataType == True:
            return node.field.getDataType()
        elif baseType == True:
            return node.field.getBaseField()
    
    def setFieldInfo(self,byte,name,abrv,description,mask,size,dataType,baseType,string):
        node = self.startNode.searchNode(name)
        if name == True:
            return node.field.setName(string)
        elif byte == True:
            return node.field.setByteSize(string)
        elif abrv == True:
            return node.field.setAbrv(string)
        elif description == True:
            return node.field.setDescription(string)
        elif mask == True:
            return node.field.setMask(string)
        elif size == True:
            return node.field.setSize(string)
        elif dataType == True:
            return node.field.setDataType(string)
        elif baseType == True:
            return node.field.setBaseField(string)