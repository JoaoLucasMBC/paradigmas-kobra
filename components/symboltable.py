from components.genericvisitor import Visitor

class SymbolTable(Visitor):
    def __init__(self):
        self.ST = {}

    def visit_main(self, main):
        main.vars.accept(self)
        if main.funcs != None:
            main.funcs.accept(self)

    def visit_funcs(self, f):
        f.func.accept(self)
        if f.funcs != None:
            f.funcs.accept(self)

    def visit_func(self, f):
        f.vars.accept(self)
        if f.arg != None:
            f.arg.accept(self)

    def visit_vars(self, v):
        v.var.accept(self)
        if v.vars != None:
            v.vars.accept(self)

    def visit_var(self, v):
        self.ST[v.id] = v.tp