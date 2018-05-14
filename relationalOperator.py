
class relationalOperator:
    def __init__(self):
        self.lessThan = "<"
        self.greaterThan = ">"
        self.lessThanOrEqualTo = "<="
        self.greaterThanOrEqualTo = ">="
        self.equalTo = "=="
        self.notEqualTo = "!="
        
    def check(self,operator):
        if operator == self.lessThan:
            return self.lessThan
        if operator == self.greaterThan:
            return self.greaterThan
        if operator == self.lessThanOrEqualTo:
            return self.lessThanOrEqualTo
        if operator == self.greaterThanOrEqualTo:
            return self.greaterThanOrEqualTo
        if operator == self.equalTo:
            return self.equalTo
        if operator == self.notEqualTo: 
            return self.notEqualTo
        else:
            print "no relational Operator"
            return None
