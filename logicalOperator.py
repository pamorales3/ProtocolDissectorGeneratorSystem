
class logicalOperator:
    def __init__(self):
        self.And = "&&"
        self.Or = "||"
        self.Not = "!"

    def check(self,operator):
        if operator == self.And:
            return self.And
        if operator == self.Or:
            return self.Or
        if operator == self.Not:
            return self.Not
        else:
            print "No operator match"
            return None
