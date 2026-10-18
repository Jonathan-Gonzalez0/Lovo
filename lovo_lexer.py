import ply.lex as lex 
import sys

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
"COMMA",
"POWER",
"POWER_UNIT"
)

t_ignore = " \t"

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
t_COMMA = r"\,"

# Power Track 
t_POWER = r"@power\b"

def t_IDENTIFIER(t):
  r"[a-zA-Z][a-zA-Z0-9_]*"

  if t.value in ("A", "mA", "J", "Wh"):
    t.type = "POWER_UNIT"
  elif t.value == "let":
    t.type = "LET"
  if t.value == "true" or t.value == "false":
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

# Illegal Characters

def t_error(t):
  char = t.value[0]

  if char == '"':
    print(f"Error: malformed string at line {t.lineno}")
  else:
    print(f"Error: unexpected token ‘{char}’ at line {t.lineno}")

  sys.exit(0)

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

lexer = lex.lex()