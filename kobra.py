# get the arguments from the command line

import sys
import os
from rply import LexerGenerator, ParserGenerator
from rply.token import BaseBox
import warnings


def main():
    # get the name of the file from the command line

    if len(sys.argv) != 2:
        print("Usage: python kobra.py <filename>")
        return
    
    filename = sys.argv[1]

    # check if the file exists
    if not os.path.exists(filename):
        print("Error: File '%s' not found" % filename)
        return
    
    with open(filename) as f:
        prog = f.read()
    
    warnings.filterwarnings("ignore")

    lexer = create_lexer()
    parser = create_parser()
 
    executor = Executor()
    symbol_table = SymbolTable()

    arvore = parser.parse(lexer.lex(prog))
    arvore.accept(symbol_table)
    arvore.accept(Decorator(symbol_table.ST))
    arvore.accept(TypeVerifier())
    arvore.accept(executor)

    print("Result:")
    print(executor.result_table)




def create_lexer():
    lg = LexerGenerator()

    lg.add('MAIN', r'main')

    lg.add('NUMBER', r'\d+(.\d+)?')
    lg.add('PLUS', r'\+')
    lg.add('MINUS', r'-')
    lg.add('MUL', r'\*')
    lg.add('DIV', r'/')
    lg.add('POW', r'\^')
    lg.add('OPEN_PARENS', r'\(')
    lg.add('CLOSE_PARENS', r'\)')

    lg.add('OPEN_CURLY', r'{')
    lg.add('CLOSE_CURLY', r'}')
    lg.add('OPEN_SQUARE', r'\[')
    lg.add('CLOSE_SQUARE', r'\]')

    lg.add('COLON', r':')

    lg.add('INT', r'int')
    lg.add('FLOAT', r'float')
    lg.add('IF', r'if')
    lg.add('ELSE', r'else')
    lg.add('WHILE', r'while')

    lg.add('ID', r'[a-zA-Z][a-zA-Z0-9]*')
    lg.add('COMP','==')
    lg.add('COMP','!=')
    lg.add('COMP','>=')
    lg.add('COMP','>')
    lg.add('COMP','<=')
    lg.add('COMP','<')

    lg.add('EQUALS', r'=')
    lg.add('ENDLINE', r';')

    lg.ignore('\s+')
    lg.ignore('//.*\n') # Comments
    lg.ignore('\t+')
    lg.ignore('\n+')

    lexer = lg.build()

    return lexer

class Main(BaseBox):
    def __init__(self, vars, instrs):
        self.vars = vars
        self.instrs = instrs

    def accept(self, visitor):
        visitor.visit_main(self)


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


def create_parser():
    pg = ParserGenerator(
    # A list of all token names, accepted by the lexer.
    ['NUMBER', 'OPEN_PARENS', 'CLOSE_PARENS', 'OPEN_CURLY', 'CLOSE_CURLY','OPEN_SQUARE', 'CLOSE_SQUARE', 'COLON',
     'PLUS', 'MINUS', 'MUL', 'DIV', 'POW', 'INT', 'FLOAT', 'ID','ENDLINE',
     'EQUALS','COMP','IF','ELSE','WHILE', 'MAIN'
    ],
    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV']),
        ('left', ['POW'])
    ]
    )

    @pg.production('main : MAIN OPEN_CURLY vars instructions CLOSE_CURLY')
    def prog(p):
        return Main(p[2],p[3])

    ##################################################
    # DECLARAÇÕES DE VARIÁVEIS
    ##################################################

    @pg.production('vars : var')
    def vars(p):
        return Vars(p[0],None)

    @pg.production('vars : var vars')
    def vars(p):
        return Vars(p[0],p[1])

    @pg.production('var : FLOAT COLON ID ENDLINE')
    def var_float(p):
        return Var(p[2].getstr(), "float")

    @pg.production('var : INT COLON ID ENDLINE')
    def var_int(p):
        return Var(p[2].getstr(), "int")

    ##################################################
    # COMANDOS - CASO ABERTO
    ##################################################

    @pg.production('instructions : openinstruction')
    def instruction_openinstruction(p):
        return Instructions(p[0],None)

    @pg.production('instructions : openinstruction instructions')
    def instruction_instructions(p):
        return Instructions(p[0],p[1])

    @pg.production('openinstruction : ID EQUALS expression ENDLINE')
    def openinstruction_atrib(p):
        return Atrib(p[0].getstr(),p[2])

    @pg.production('openinstruction : IF OPEN_PARENS expression COMP expression CLOSE_PARENS OPEN_CURLY openinstruction CLOSE_CURLY')
    def expression_ifelse1(p):
        return IfElse (p[2],p[3],p[4],p[7],None)

    @pg.production('openinstruction : IF OPEN_PARENS expression COMP expression CLOSE_PARENS OPEN_CURLY closedinstruction CLOSE_CURLY ELSE OPEN_CURLY openinstruction CLOSE_CURLY')
    def expression_ifelse2(p):
        return IfElse (p[2],p[3],p[4],p[7],p[11])

    @pg.production('openinstruction : WHILE OPEN_PARENS expression COMP expression CLOSE_PARENS OPEN_CURLY instructions CLOSE_CURLY')
    def instruction_while(p):
        return While (p[2],p[3],p[4],p[7])


    ##################################################
    # COMANDOS - CASO FECHADO
    ##################################################

    @pg.production('closedinstruction : ID EQUALS expression ENDLINE')
    def instruction_atrib(p):
        return Atrib(p[0].getstr(),p[2])

    @pg.production('closedinstruction : IF OPEN_PARENS expression COMP expression CLOSE_PARENS OPEN_CURLY closedinstruction CLOSE_CURLY ELSE OPEN_CURLY closedinstruction CLOSE_CURLY')
    def expression_ifelse1(p):
        return IfElse (p[2],p[3],p[4],p[7],p[11])

    @pg.production('closedinstruction : WHILE OPEN_PARENS expression COMP expression CLOSE_PARENS OPEN_CURLY closedinstruction CLOSE_CURLY')
    def instruction_while(p):
        return While (p[2],p[3],p[4],p[7])

    @pg.production('expression : ID')
    def expression_id(p):
        return Id(p[0].getstr())

    @pg.production('expression : NUMBER')
    def expression_number(p):
        # Verifica se é float ou int para fazer o casting
        value = p[0].getstr()

        if "." in value:
            value = float(value)
        else:
            value = int(value)

        return Number(value)

    @pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
    def expression_parens(p):
        return p[1]

    @pg.production('expression : expression PLUS expression')
    @pg.production('expression : expression MINUS expression')
    @pg.production('expression : expression MUL expression')
    @pg.production('expression : expression DIV expression')
    @pg.production('expression : expression POW expression')
    def expression_binop(p):
        left = p[0]
        right = p[2]
        if p[1].gettokentype() == 'PLUS':
            return Add(left, right)
        elif p[1].gettokentype() == 'MINUS':
            return Sub(left, right)
        elif p[1].gettokentype() == 'MUL':
            return Mul(left, right)
        elif p[1].gettokentype() == 'DIV':
            return Div(left, right)
        elif p[1].gettokentype() == 'POW':
            return Pow(left, right)
        else:
            raise AssertionError('Oops, this should not be possible!')

    parser = pg.build()
    return parser


class Visitor(object):
    pass

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



class Decorator(Visitor):
    def __init__(self, ST):
        self.ST = ST

    def visit_main(self, p):
        p.instrs.accept(self)

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

    def visit_ifelse(self, i):
        pass

    def visit_while(self, i):
        pass



class Executor(Visitor):
    def __init__(self):
        self.result_table = {}
        self.curr_res = []

    def visit_main(self, main):
        main.vars.accept(self)
        main.instrs.accept(self)

    def visit_vars(self, vars):
        vars.var.accept(self)
        if vars.vars:
            vars.vars.accept(self)

    def visit_var(self, var):
        self.result_table[var.id] = None

    def visit_instructions(self, instructions):
        instructions.instr.accept(self)
        if instructions.instrs:
            instructions.instrs.accept(self)
    
    def visit_instruction(self, instruction):
        instruction.instr.accept(self)

    def visit_atrib(self, atrib):
        atrib.expr.accept(self)
        value = self.curr_res.pop()
        self.result_table[atrib.id] = value


    def visit_ifelse(self, ifelse):
        ifelse.expr1.accept(self)
        ifelse.expr2.accept(self)

        e2 = self.curr_res.pop()
        e1 = self.curr_res.pop()

        condition_value = self.evaluate_comp(ifelse.comp, e1, e2)

        if condition_value:
            ifelse.ie1.accept(self)
        elif ifelse.ie2:
            ifelse.ie2.accept(self)
    
    def visit_while(self, w):
        w.expr1.accept(self)
        w.expr2.accept(self)

        e2 = self.curr_res.pop()
        e1 = self.curr_res.pop()

        condition_value = self.evaluate_comp(w.comp, e1, e2)

        while condition_value:
            w.ie1.accept(self)
            w.expr1.accept(self)
            w.expr2.accept(self)

            e2 = self.curr_res.pop()
            e1 = self.curr_res.pop()

            condition_value = self.evaluate_comp(w.comp, e1, e2)
    
    def evaluate_comp(self, comp, left, right):
        comp = comp.getstr()
        if comp == '==':
            return left == right
        elif comp == '!=':
            return left != right
        elif comp == '>=':
            return left >= right
        elif comp == '>':
            return left > right
        elif comp == '<=':
            return left <= right
        elif comp == '<':
            return left < right
        else:
            raise AssertionError('Oops, this should not be possible!')

    
    def visit_number(self, number):
        self.curr_res.append(number.value)
    
    def visit_id(self, id):
        self.curr_res.append(self.result_table[id.value])

    def visit_add(self, add):
        add.left.accept(self)
        add.right.accept(self)
        right_value = self.curr_res.pop()
        left_value = self.curr_res.pop()
        self.curr_res.append(left_value + right_value)

    def visit_sub(self, sub):
        sub.left.accept(self)
        sub.right.accept(self)
        right_value = self.curr_res.pop()
        left_value = self.curr_res.pop()
        self.curr_res.append(left_value - right_value)

    def visit_mul(self, mul):
        mul.left.accept(self)
        mul.right.accept(self)
        right_value = self.curr_res.pop()
        left_value = self.curr_res.pop()
        self.curr_res.append(left_value * right_value)
    
    def visit_div(self, div):
        div.left.accept(self)
        div.right.accept(self)
        right_value = self.curr_res.pop()
        left_value = self.curr_res.pop()
        self.curr_res.append(left_value / right_value)
    
    def visit_pow(self, pow):
        pow.left.accept(self)
        pow.right.accept(self)
        right_value = self.curr_res.pop()
        left_value = self.curr_res.pop()
        self.curr_res.append(left_value ** right_value)


if __name__ == '__main__':
    main()