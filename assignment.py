import ply.lex as lex
import ply.yacc as yacc

# Define the list of token names
tokens = (
    'IDENTIFIER',
    'ASSIGN',
    'LEFT_ARROW',
    'NUMBER',
    'STRING',
    'TRUE',
    'FALSE',
    'LPAREN',
    'RPAREN',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
)

# Define token regular expressions
t_ASSIGN = r'='
t_LEFT_ARROW = r'<-'
t_NUMBER = r'-?\d+(\.\d+)?'  # Updated to handle negative numbers
t_STRING = r'"[^"]*"|\'[^\']*\''
t_TRUE = r'TRUE'
t_FALSE = r'FALSE'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'

# Define token rules for IDENTIFIER
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Define regular expressions for LPAREN and RPAREN
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Define error handling for invalid characters
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Define precedence and associativity
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Define the grammar rules
def p_Assignment(p):
    '''Assignment : IDENTIFIER ASSIGN Expression
                  | IDENTIFIER LEFT_ARROW Expression'''
    p[0] = ('assignment', p[1], p[3])

def p_Expression(p):
    '''Expression : Comparison'''
    p[0] = p[1]

def p_Comparison(p):
    '''Comparison : Term
                  | Comparison PLUS Term
                  | Comparison MINUS Term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_Term(p):
    '''Term : Factor
            | Term TIMES Factor
            | Term DIVIDE Factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_Factor(p):
    '''Factor : Primary'''
    p[0] = p[1]

def p_Primary(p):
    '''Primary : IDENTIFIER
               | NUMBER
               | STRING
               | TRUE
               | FALSE
               | LPAREN Expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_error(p):
    print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}'")

def t_SPACE(t):
    r'[\s\t]+'
    pass  # No return value, so we skip spaces and tabs


# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Test the parser with an R assignment expression
code = 'x <- -5'
parsed = parser.parse(code)
print(parsed)
