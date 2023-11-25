from components.genericvisitor import Visitor
from components.nodes import Expr

class TypeVerifier(Visitor):

    def visit_main(self, i):
        i.instrs.accept(self)

    def visit_instructions(self, d):
        d.instr.accept(self)
        if d.instrs!=None:
            d.instrs.accept(self)

    def visit_instruction(self, d):
        d.instr.accept(self)

    def visit_atrib(self, i):
        if i.decor_type != i.expr.decor_type:
            raise AssertionError(f'type {i.expr.decor_type} cannot be assigned to {i.decor_type}')
    
    def visit_print(self, i):
        if isinstance(i.value, Expr):
            i.value.accept(self)

    def visit_ifelse(self, i):
        pass

    def visit_while(self, i):
        pass