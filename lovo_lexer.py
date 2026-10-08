import ply.lex as lex 

tokens = (
"LET",
"BOOL",
"STRING",
"EXP",
"INTEGER",
"FLOAT",
"PLUS",
"MINUS",
"TIMES",
"DIVIDE",
"MODULO",
"LPAREN",
"RPAREN",
"LBRACE",
"RBRACE",
"IDENTIFIER",
"ASSIGN",
"EQUALS",
"NEQUALS",
"LTE",
"LT",
"GTE",
"GT",
"IF",
"ELSE",
"WHILE",
"FOR",
"SEMICOLON",
"FUNC",
"RETURN",
"PRINT",
"COMMENT"
)

t_ignore = " "

# Program Types
t_INTEGER = r"\d+"

t_FLOAT = r"\d+\.\d+"

t_STRING = r'"[^"\r\n]*"'

# Arithmetic Operations

t_EXP = r"\*\*"

t_TIMES = r"\*"

t_DIVIDE = r"\/"

t_MODULO = r"\%"

t_PLUS = r"\+"

t_MINUS = r"\-"

# Comparison Operators

t_EQUALS = r"\=="

t_NEQUALS = r"\!="

t_LTE = r"\<="

t_LT = r"\<"

t_GTE = r">="

t_GT = r">"

# Enclosures

t_LPAREN = r"\("

t_RPAREN = r"\)"

t_LBRACE = r"\{"

t_RBRACE = r"\}"


# Comments

t_ignore_COMMENT = r"\//[^\r\n]*"

# Misc 

t_SEMICOLON = r"\;"
t_ASSIGN = r"\="

def t_IDENTIFIER(t):
  r"[a-zA-z]+"
  if t.value == "let":
    t.type = "LET"
  if t.value == "True" or t.value == "False":
    t.type = "BOOL"
  if t.value == "if":
    t.type = "IF"
  if t.value == "else":
    t.type = "ELSE"
  if t.value == "while":
    t.type = "WHILE"
  if t.value == "for":
    t.type = "FOR"
  if t.value == "func":
    t.type = "FUNC"
  if t.value == "return":
    t.type = "RETURN"
  if t.value == "print":
    t.type = "PRINT"
  return t

lexer = lex.lex()

lexer.input("(375 + 82 - 15) / 20.0")

lexer.input("(2*2)**8 % 4")

lexer.input("x = 8")

lexer.input("let Result = 8")

lexer.input("let Result = False")

lexer.input('let Result = "Hi~" ')

lexer.input('Result == 10')

lexer.input('Result <= 10')

lexer.input('Result < 10')

lexer.input('Result >= 10')

lexer.input('Result > 10')

lexer.input('Result != 10')

lexer.input("if(Result){ x } else { 0 }")

lexer.input("while(Result){ x += 1}")

lexer.input("for(let i = 0; i < 5; i = i + 1){ Result = i}")

lexer.input("func")

lexer.input("return")

lexer.input("print(x);")

lexer.input("// aaa")

token = lexer.token()

while token is not None:
  print(token)
  token = lexer.token()
  
print("Ply is ready")