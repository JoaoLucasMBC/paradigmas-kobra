from rply.token import BaseBox

class Main(BaseBox):
    def __init__(self, vars, instrs, funcs):
        self.vars = vars
        self.instrs = instrs
        self.funcs = funcs

    def accept(self, visitor):
        visitor.visit_main(self)

## FUNCTIONS

class Funcs(BaseBox):
    def __init__(self, func, funcs):
        self.func = func
        self.funcs = funcs

    def accept(self, visitor):
        visitor.visit_funcs(self)

class Func(BaseBox):
    def __init__(self, ret_type, id, arg, vars, instrs, ret):
       self.ret_type = ret_type
       self.id = id
       self.arg = arg
       self.vars = vars
       self.instrs = instrs
       self.ret = ret

    def accept(self, visitor):
        visitor.visit_func(self)

## RESTO


class Vars(BaseBox):
    def __init__(self, var, vars):
        self.var = var
        self.vars = vars

    def accept(self, visitor):
        visitor.visit_vars(self)

class Var(BaseBox):
    def __init__(self, id, tp):
        self.id = id
        self.tp = tp

    def accept(self, visitor):
        visitor.visit_var(self)


class Instructions(BaseBox):
    def __init__(self, instr, instrs):
        self.instr = instr
        self.instrs = instrs

    def accept(self, visitor):
        visitor.visit_instructions(self)

class Instruction(BaseBox):
    def __init__(self, instr):
        self.instr = instr

    def accept(self, visitor):
        visitor.visit_instruction(self)


class Atrib(BaseBox):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_atrib(self)

class IfElse(BaseBox):
    def __init__(self, expr1, comp, expr2, ie1,ie2):
        self.expr1=expr1
        self.comp = comp
        self.expr2=expr2
        self.ie1=ie1
        self.ie2=ie2

    def accept(self, visitor):
        visitor.visit_ifelse(self)

class While(BaseBox):
    def __init__(self, expr1, comp, expr2, ie1):
        self.expr1=expr1
        self.comp = comp
        self.expr2=expr2
        self.ie1=ie1

    def accept(self, visitor):
        visitor.visit_while(self)

class Print(BaseBox):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.visit_print(self)

class Expr(BaseBox):
    def accept(self, visitor):
        method_name = 'visit_{}'.format(self.__class__.__name__.lower())
        visit = getattr(visitor, method_name)
        visit(self)

class Id(Expr):
    def __init__(self, value):
        self.value = value

class Number(Expr):
    def __init__(self, value):
        self.value = value

## CALLING A FUNCTIONS IS AN EXPRESSION
class Call(Expr):
    def __init__(self, func_id, arg):
        self.func_id = func_id
        self.arg = arg

class Return(BaseBox):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        visitor.visit_return(self)

## RESTO


class BinaryOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryOp):
    pass


class Sub(BinaryOp):
    pass


class Mul(BinaryOp):
    pass


class Div(BinaryOp):
    pass

class Pow(BinaryOp):
    pass