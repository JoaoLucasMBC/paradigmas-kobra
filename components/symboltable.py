from components.genericvisitor import Visitor

class SymbolTable(Visitor):
    def __init__(self):
        self.ST = {}

    def visit_main(self, main):
        main.vars.accept(self)

    def visit_vars(self, v):
        v.var.accept(self)
        if v.vars != None:
            v.vars.accept(self)

    def visit_var(self, v):
        self.ST[v.id] = v.tp