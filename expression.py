from relationalOperator import *
from logicalOperator import *

class expression:
    def __init__(self):
        self.operand = None
        self.relationalOperator = None
        self.logicalOperator = None

    def getRelationalOperator(self):
        return self.relationalOperator
    def getLogicalOperator(self):
        return self.logicalOperator
    def getOperand(self):
        return self.operand
    def setRelationalOperator(self,operator):
        temp = relationalOperator()
        self.relationalOperator = temp.check(operator)

    def setLogicalOperator(self,operator):
        temp = logicalOperator()
        self.logicalOperator = temp.check(operator)

    def setOperand(self, operand):
        self.operand = operand
    
