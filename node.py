from decisionConstruct import *
from field import *
from os import *
import xml.etree.ElementTree as et
class node:
    def __init__(self,name):
        self.name = name
        self.nextNode = None
        self.expression = expression()
        self.field = field()


    def addDecisionNode(self,true,false):
        next = self.nextNode
        create = decisionConstruct(true,false)
        create.falseNode.nextNode = next
        create.trueNode.nextNode = next
        self.nextNode = create

    def createList(self):
        current = self
        next = current.nextNode
        if next.name == "dc":
            list1 = next.falseNode.createList()
            list2 = next.trueNode.createList()
            list = [current.name,list1,list2]
            return list
        elif next.name == "end":
            list = [current.name,"end"]
            return list
        elif next != None:
            list1 = next.createList()
            list = [current.name,list1]
            return list
        

    def addNode(self,node):
        if self.nextNode != None:
            next = self.nextNode
            self.nextNode = node
            node.nextNode = next
        else:
            self.nextNode = node

    def createXML(self,root,num):
        current = self
        next = current.nextNode
        field = et.SubElement(root, self.field.getName(), attrib = {"id": str(num)})
        fieldName = et.SubElement(field,"name")
        fieldAbrv = et.SubElement(field,"abrv")
        fieldByteSize = et.SubElement(field,"byteSize")
        fieldDescription = et.SubElement(field,"desciption")
        fieldMask = et.SubElement(field,"mask")
        fieldSize = et.SubElement(field,"size")
        fieldDataType = et.SubElement(field,"dataType")
        fieldBaseType = et.SubElement(field,"baseType")
        fieldName.text = self.field.getName()
        fieldAbrv.text = self.field.getAbrv()
        fieldByteSize = self.field.getByteSize()
        fieldDescription = self.field.getDescription()
        fieldMask = self.field.getMask
        fieldSize = self.field.getSize
        fieldDataType = self.field.getDataType
        fieldBaseType = self.field.getBaseType
        if next.name == "end":
            print "end"
        elif next.name == "dc":
            next.trueNode.createXML(root,num+1)
            next.falseNode.createXML(root,num+2)
        else:
            next.createXML(root,num+1)


    def searchNode(self,name):
        current = self
        next = current.nextNode
        if current.name == name:
            return current
        elif next.name == "end":
            return next
        elif next.name == "dc":
            return next.falseNode.searchNode(name)
            return next.trueNode.searchNode(name)
        elif next != None:
            return next.searchNode(name)