from components.genericvisitor import Visitor

class FuncTable(Visitor):
    def __init__(self):
        self.FT = {}

    def visit_main(self, main):
        if main.funcs != None:
            main.funcs.accept(self)

    def visit_funcs(self, f):
        f.func.accept(self)
        if f.funcs != None:
            f.funcs.accept(self)

    def visit_func(self, f):
        self.FT[f.id] = f