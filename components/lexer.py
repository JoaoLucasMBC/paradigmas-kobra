def create_lexer():
    from rply import LexerGenerator

    lg = LexerGenerator()

    lg.add('MAIN', r'main')

    lg.add('NUMBER', r'\d+(.\d+)?')
    lg.add('PLUS', r'\+')
    lg.add('MINUS', r'-')
    lg.add('MUL', r'\*')
    lg.add('DIV', r'/')
    lg.add('POW', r'\^')
    lg.add('PRINT', r'print')
    lg.add('RETURN', r'return')
    lg.add('OPEN_PARENS', r'\(')
    lg.add('CLOSE_PARENS', r'\)')

    lg.add('OPEN_CURLY', r'{')
    lg.add('CLOSE_CURLY', r'}')
    lg.add('OPEN_SQUARE', r'\[')
    lg.add('CLOSE_SQUARE', r'\]')

    lg.add('COLON', r':')

    lg.add('VOID', r'void')
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

    lg.add('STRING', r'\".*\"')

    lg.ignore('\s+')
    lg.ignore('//.*\n')
    lg.ignore('\t+')
    lg.ignore('\n+')

    lexer = lg.build()
    return lexer