# get the arguments from the command line

import sys
import os

from components.executor import Executor
from components.symboltable import SymbolTable
from components.decorator import Decorator
from components.typeverifier import TypeVerifier
from components.lexer import create_lexer
from components.parser import create_parser

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
    
    lexer = create_lexer()
    parser = create_parser()
 
    executor = Executor()
    symbol_table = SymbolTable()

    print("RUNTIME:")
    arvore = parser.parse(lexer.lex(prog))
    arvore.accept(symbol_table)
    arvore.accept(Decorator(symbol_table.ST))
    arvore.accept(TypeVerifier())
    arvore.accept(executor)
    print("")

    print("Result:")
    print(executor.result_table)

if __name__ == '__main__':
    main()