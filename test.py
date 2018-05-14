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
test.getXMl()


print test
print node.name

