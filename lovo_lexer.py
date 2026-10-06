import ply.lex as lex 

tokens = (
"INTEGER",
"PLUS",
"MINUS",
)

t_ignore = " "

t_INTEGER = r"\d+"

t_PLUS = r"\+"

t_MINUS = r"\-"

lexer = lex.lex()

lexer.input("375 + 82 - 15")

token = lexer.token()

while token is not None:
  print(token)
  token = lexer.token()


print("Ply is ready")