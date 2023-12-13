from components.genericvisitor import Visitor
from components.nodes import Expr

class Decorator(Visitor):
    def __init__(self, ST, FT):
        self.ST = ST
        self.FT = FT

    def visit_main(self, p):
        p.instrs.accept(self)
        if p.funcs != None:
            p.funcs.accept(self)

    def visit_funcs(self, f):
        f.func.accept(self)
        if f.funcs != None:
            f.funcs.accept(self)

    def visit_func(self, f):
        f.instrs.accept(self)
        f.ret.accept(self)

    def visit_instructions(self, i):
        i.instr.accept(self)
        if i.instrs!=None:
            i.instrs.accept(self)

    def visit_instruction(self, i):
        i.instr.accept(self)

    def visit_atrib(self, i):
        if i.id in self.ST:
          i.decor_type = self.ST[i.id]
        else:
          raise AssertionError('id not declared')
        i.expr.accept(self)

    def visit_print(self, i):
        if isinstance(i.value, Expr):
            i.value.accept(self)

    def visit_ifelse(self, i):
        i.expr1.accept(self)
        i.expr2.accept(self)
        i.ie1.accept(self)
        if i.ie2!=None:
          i.ie2.accept(self)

    def visit_while(self, i):
        i.expr1.accept(self)
        i.expr2.accept(self)
        i.ie1.accept(self)

    def visit_return(self, r):
        if r.expr != None:
          r.expr.accept(self)
          r.decor_type = r.expr.decor_type
        else:
          r.decor_type = 'void'

    def visit_call(self, c):
        if not c.func_id in self.FT:
          raise AssertionError('function not declared')
        c.decor_type = self.FT[c.func_id].ret_type

    def visit_id(self, i):
        if i.value in self.ST:
          i.decor_type = self.ST[i.value]
        else:
          raise AssertionError('id not declared')

    def visit_number(self, i):
        if "." in str(i.value):
          i.decor_type='float'
        else:
          i.decor_type='int'


    # Segue as regras de operação
    # INT op INT = INT
    # INT op FLOAT = FLOAT
    # FLOAT op FLOAT = FLOAT
    def visit_add(self, a):
        a.left.accept(self)
        a.right.accept(self)
        if a.left.decor_type=="float" or a.right.decor_type=="float":
          a.decor_type="float"
        else:
          a.decor_type="int"


    def visit_sub(self, a):
        a.left.accept(self)
        a.right.accept(self)
        if a.left.decor_type=="float" or a.right.decor_type=="float":
          a.decor_type="float"
        else:
          a.decor_type="int"

    def visit_mul(self, a):
        a.left.accept(self)
        a.right.accept(self)
        if a.left.decor_type =="float" or a.right.decor_type=="float":
          a.decor_type="float"
        else:
          a.decor_type="int"

    def visit_div(self, a):
        a.left.accept(self)
        a.right.accept(self)
        if a.left.decor_type=="float" or a.right.decor_type=="float":
          a.decor_type="float"
        else:
          a.decor_type="int"

    def visit_pow(self, a):
        a.left.accept(self)
        a.right.accept(self)
        if a.left.decor_type=="float" or a.right.decor_type=="float":
            a.decor_type="float"
        else:
            a.decor_type="int"