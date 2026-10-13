import sys
from cli import command_line_interface
import ply.yacc as yacc
from lovo_lexer import tokens, lexer

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

def p_statement_power_function(p):
    'statement : POWER LPAREN INTEGER POWER_UNIT RPAREN FUNC IDENTIFIER LPAREN parameters_opt RPAREN block'
    p[0] = ("power_function", p[3], p[4], p[7], p[9], p[11])

def p_statement_power_function_float(p):
    'statement : POWER LPAREN FLOAT POWER_UNIT RPAREN FUNC IDENTIFIER LPAREN parameters_opt RPAREN block'
    p[0] = ("power_function", p[3], p[4], p[7], p[9], p[11])


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

def p_condition(p):
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

def p_expression_comparison(p):
    'expression : arithmetic_expression comparison_operator arithmetic_expression'
    p[0] = (p[2], p[1], p[3])


def p_arithmetic_expression(p):
    'expression : arithmetic_expression'
    p[0] = p[1]


def p_arithmetci_plus(p):
    'arithmetic_expression : arithmetic_expression PLUS term'
    p[0] = ("+", p[1], p[3])


def p_expression_minus(p):
    'arithmetic_expression : arithmetic_expression MINUS term'
    p[0] = ("-", p[1], p[3])


def p_expression_term(p):
    'arithmetic_expression : term'
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

def p_factor_function_call(p):
    'factor : IDENTIFIER LPAREN arguments_optional RPAREN'
    p[0] = ("function_call", p[1], p[3])

def p_arguments_single(p):
    'arguments : expression'
    p[0] = [p[1]]

def p_arguments_multiple(p):
    'arguments : arguments COMMA expression'
    p[0] = p[1] + [p[3]]

def p_arguments_optional(p):
    '''arguments_optional : arguments
                     | empty'''
    p[0] = [] if p[1] is None else p[1]

# Error handling

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print(f"Syntax error at end of input (line {lexer.lineno})")
    sys.exit(1)

# Success message

def print_success():
    print("Parse successful!")

# Interpreter
variables = {}
  
def evaluate(node):
    if isinstance(node, (int,float)):
        return node

    kind = node[0]

    if kind == "identifier":
        name = node[1]

        if name not in variables:
            raise NameError(f"Undefined variable: {name}")

        return variables[name]

    if kind == "+":
        left = evaluate(node[1])
        right = evaluate(node[2])
        return left + right

    raise ValueError(f"Unsupported expression: {node}")

def execute(node):
    kind = node[0]

    if kind == "program":
        for statement in node[1]:
            execute(statement)

    elif kind == "declare":
        name = node[1]
        value = evaluate(node[2])
        variables[name] = value

    elif kind == "print":
        print(evaluate(node[1]))

parser = yacc.yacc()

if __name__ == "__main__":
    code = command_line_interface()

    lexer.lineno = 1
    result = parser.parse(code, lexer=lexer)

    if result is not None:
        print_success()


 