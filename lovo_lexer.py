import ply.lex as lex 

tokens = (
"LET",
"BOOL",
"STRING",
"LPAREN",
"RPAREN",
"EXP",
"INTEGER",
"FLOAT",
"PLUS",
"MINUS",
"TIMES",
"DIVIDE",
"MODULO",
"IDENTIFIER",
"ASSIGN"
)

t_ignore = " "

#Program Types
t_INTEGER = r"\d+"

t_FLOAT = r"\d+\.\d+"

t_STRING = r'"[^"\r\n]*"'

t_LPAREN = r"\("

t_RPAREN = r"\)"

t_EXP = r"\*\*"

t_TIMES = r"\*"

t_DIVIDE = r"\/"

t_MODULO = r"\%"

t_PLUS = r"\+"

t_MINUS = r"\-"

def t_IDENTIFIER(t):
  r"[a-zA-z]+"
  if t.value == "let":
    t.type = "LET"
  if t.value == "True" or t.value == "False":
    t.type = "BOOL"
  return t

t_ASSIGN = r"\="

lexer = lex.lex()

lexer.input("(375 + 82 - 15) / 20.0")

lexer.input("(2*2)**8 % 4")

lexer.input("x = 8")

lexer.input("let Result = 8")

lexer.input("let Result = False")

lexer.input('let Result = "Hi~" ')

token = lexer.token()

while token is not None:
  print(token)
  token = lexer.token()
  
print("Ply is ready")