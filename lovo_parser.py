import sys
import ply.yacc as yacc
from lovo_lexer import tokens

# PARSER
def p_program(p):
    'program : statements'
    p[0] = ("program", p[1])


def p_statements_single(p):
    'statements : statement'
    p[0] = [p[1]]


def p_statements_multiple(p):
    'statements : statements statement'
    p[0] = p[1] + [p[2]]


# Statements

def p_statement_expression(p):
    'statement : expression SEMICOLON'
    p[0] = p[1]


def p_statement_declaration(p):
    'statement : LET IDENTIFIER ASSIGN expression SEMICOLON'
    p[0] = ("declare", p[2], p[4])


def p_statement_assignment(p):
    'statement : assignment SEMICOLON'
    p[0] = p[1]


def p_assignment(p):
    'assignment : IDENTIFIER ASSIGN expression'
    p[0] = ("assign", p[1], p[3])


def p_statement_print(p):
    'statement : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0] = ("print", p[3])


def p_statement_return(p):
    'statement : RETURN expression SEMICOLON'
    p[0] = ("return", p[2])


def p_statement_if(p):
    'statement : IF LPAREN condition RPAREN block'
    p[0] = ("if", p[3], p[5], None)


def p_statement_if_else(p):
    'statement : IF LPAREN condition RPAREN block ELSE block'
    p[0] = ("if", p[3], p[5], p[7])


def p_statement_while(p):
    'statement : WHILE LPAREN condition RPAREN block'
    p[0] = ("while", p[3], p[5])


def p_statement_for(p):
    'statement : FOR LPAREN for_init SEMICOLON condition SEMICOLON assignment RPAREN block'
    p[0] = ("for", p[3], p[5], p[7], p[9])


def p_for_init_declaration(p):
    'for_init : LET IDENTIFIER ASSIGN expression'
    p[0] = ("declare", p[2], p[4])


def p_for_init_assignment(p):
    'for_init : assignment'
    p[0] = p[1]


def p_statement_function(p):
    'statement : FUNC IDENTIFIER LPAREN parameters_opt RPAREN block'
    p[0] = ("function", p[2], p[4], p[6])


def p_parameters_one(p):
    'parameters : IDENTIFIER'
    p[0] = [p[1]]


def p_parameters_multiple(p):
    'parameters : parameters COMMA IDENTIFIER'
    p[0] = p[1] + [p[3]]


def p_parameters_opt(p):
    '''parameters_opt : parameters
                      | empty'''
    p[0] = [] if p[1] is None else p[1]


# Blocks

def p_block(p):
    'block : LBRACE statements_opt RBRACE'
    p[0] = p[2]


def p_statements_opt(p):
    '''statements_opt : statements
                      | empty'''
    p[0] = [] if p[1] is None else p[1]


def p_empty(p):
    'empty :'
    p[0] = None


# Conditions and comparisons

def p_condition_comparison(p):
    'condition : expression comparison_operator expression'
    p[0] = (p[2], p[1], p[3])


def p_condition_expression(p):
    'condition : expression'
    p[0] = p[1]


def p_comparison_operator(p):
    '''comparison_operator : EQUALS
                           | NEQUALS
                           | LTE
                           | LT
                           | GTE
                           | GT'''
    p[0] = p[1]


# Expressions

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = ("+", p[1], p[3])


def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = ("-", p[1], p[3])


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_times(p):
    'term : term TIMES power'
    p[0] = ("*", p[1], p[3])


def p_term_divide(p):
    'term : term DIVIDE power'
    p[0] = ("/", p[1], p[3])


def p_term_modulo(p):
    'term : term MODULO power'
    p[0] = ("%", p[1], p[3])


def p_term_power(p):
    'term : power'
    p[0] = p[1]


def p_power_exp(p):
    'power : factor EXP power'
    p[0] = ("**", p[1], p[3])


def p_power_factor(p):
    'power : factor'
    p[0] = p[1]


# Values

def p_factor_integer(p):
    'factor : INTEGER'
    p[0] = int(p[1])


def p_factor_float(p):
    'factor : FLOAT'
    p[0] = float(p[1])


def p_factor_string(p):
    'factor : STRING'
    p[0] = p[1]


def p_factor_bool(p):
    'factor : BOOL'
    p[0] = p[1] == "True"


def p_factor_identifier(p):
    'factor : IDENTIFIER'
    p[0] = ("identifier", p[1])


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


# Error handling

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at end of input")


parser = yacc.yacc()

if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        code = file.read()

    result = parser.parse(code)
    print(result)


 