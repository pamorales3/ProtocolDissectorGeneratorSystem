from node import *
from endNode import *
from protocolDecisionTreeConstruct import *

t = node("t")
b = node("b")
h = node("h")
hi = node("hi")
hs= node("hs")
ha=node("ha")
end = endNode()

test = protocolDecisionTreeConstruct()
test.addNewNode(t,"start")
test.addDecisionNode(ha,hs,"t")
node = test.createNode("his")
test.setFieldInfo(False,False,True,False,False,"t","hi")
test1 = test.getFieldInfo(False,False,True,False,False,"t")
test = test.createList()
print test
print node.name
