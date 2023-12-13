from components.genericvisitor import Visitor
from components.nodes import Expr, Call

class TypeVerifier(Visitor):
    def __init__(self, ST, FT):
        self.ST = ST
        self.FT = FT

    def visit_main(self, i):
        i.instrs.accept(self)
        if i.funcs != None:
          i.funcs.accept(self)

    def visit_funcs(self, f):
        f.func.accept(self)
        if f.funcs != None:
          f.funcs.accept(self)

    def visit_func(self, f):
        f.instrs.accept(self)
        if f.ret_type != f.ret.decor_type:
            raise AssertionError(f'cannot return expression of type {f.ret.decor_type} if the return type of the function is {f.ret_type}')

    def visit_instructions(self, d):
        d.instr.accept(self)
        if d.instrs!=None:
            d.instrs.accept(self)

    def visit_instruction(self, d):
        d.instr.accept(self)

    def visit_call(self, c):
        # O argumento do call tem que ter o mesmo tipo do argumento da função
        if c.arg != None and self.ST[c.arg] != self.ST[self.FT[c.func_id].arg.id]:
            raise AssertionError(f'cannot pass variable of type {self.ST[c.arg]} to function that accepts type {self.FT[c.func_id].arg.tp}')

    def visit_return(self, r):
        pass ## todas as checagens do return acontecem na checagem da função ou na checagem da atribuição

    def visit_atrib(self, i):
        if isinstance(i.expr, Call):
            i.expr.accept(self)
            if i.decor_type != self.FT[i.expr.func_id].ret.decor_type:
              raise AssertionError(f'return type {self.FT[i.expr.func_id].ret.decor_type} cannot be assigned to variable of type {i.decor_type}')
        if i.decor_type != i.expr.decor_type:
            raise AssertionError(f'expression type {i.expr.decor_type} cannot be assigned to variable of type {i.decor_type}')

    def visit_print(self, i):
        pass

    def visit_ifelse(self, i):
        pass

    def visit_while(self, i):
        pass