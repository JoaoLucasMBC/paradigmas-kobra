from components.nodes import *

def create_parser():
    from rply import ParserGenerator

    pg = ParserGenerator(
        # A list of all token names, accepted by the lexer.
        ['NUMBER', 'OPEN_PARENS', 'CLOSE_PARENS', 'OPEN_CURLY', 'CLOSE_CURLY','OPEN_SQUARE', 'CLOSE_SQUARE', 'COLON',
        'PLUS', 'MINUS', 'MUL', 'DIV', 'POW', 'INT', 'FLOAT', 'ID','ENDLINE',
        'EQUALS','COMP','IF','ELSE','WHILE', 'MAIN', 'PRINT', 'STRING'
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

    @pg.production('openinstruction : PRINT OPEN_PARENS STRING CLOSE_PARENS ENDLINE')
    def print_instruction(p):
        return Print(p[2].getstr())

    @pg.production('openinstruction : PRINT OPEN_PARENS expression CLOSE_PARENS ENDLINE')
    def print_instruction(p):
        return Print(p[2])

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

    @pg.production('closedinstruction : PRINT OPEN_PARENS STRING CLOSE_PARENS ENDLINE')
    def print_instruction(p):
        return Print(p[2].getstr())

    @pg.production('closedinstruction : PRINT OPEN_PARENS expression CLOSE_PARENS ENDLINE')
    def print_instruction(p):
        return Print(p[2])


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