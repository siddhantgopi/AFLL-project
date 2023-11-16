import ply.lex as lex
import ply.yacc as yacc

# Define the list of token names
tokens = (
    'WHILE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'TRUE',
    'FALSE',
    'IDENTIFIER',
    'NUMBER',
    'NOT',
    'EQ',
    'NE',
    'LT',
    'LE',
    'GT',
    'GE',
    'ASSIGN',
    'LEFT_ARROW',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
)

# Define token regular expressions
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_TRUE = r'TRUE'
t_FALSE = r'FALSE'
t_NOT = r'!'
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_ASSIGN = r'<-'
t_LEFT_ARROW = r'<-'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'


# Define the 'WHILE' token rule
def t_WHILE(t):
    r'while'
    return t

# Define token rules for IDENTIFIER and NUMBER
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Define error handling for invalid characters
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Define precedence and associativity
precedence = (
    ('left', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Define the grammar rules
def p_WhileLoop(p):
    '''WhileLoop : WHILE LPAREN Expression RPAREN Block'''
    p[0] = ('while', p[3], p[5])

def p_Block(p):
    '''Block : LBRACE Statements RBRACE
             | Statement'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_Statements(p):
    '''Statements : Statement
                  | Statements Statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_Statement(p):
    '''Statement : WhileLoop
                | Assignment'''
    p[0] = p[1]

def p_Assignment(p):
    '''Assignment : IDENTIFIER ASSIGN Expression
                  | IDENTIFIER LEFT_ARROW Expression'''
    p[0] = ('assignment', p[1], p[3])

def p_Expression(p):
    '''Expression : Comparison'''
    p[0] = p[1]

def p_Comparison(p):
    '''Comparison : Term
                  | Comparison EQ Term
                  | Comparison NE Term
                  | Comparison LT Term
                  | Comparison LE Term
                  | Comparison GT Term
                  | Comparison GE Term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_Term(p):
    '''Term : Factor
            | Term PLUS Factor
            | Term MINUS Factor
            | Term TIMES Factor
            | Term DIVIDE Factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])

def p_Factor(p):
    '''Factor : Primary
              | NOT Factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('not', p[2])

def p_Primary(p):
    '''Primary : IDENTIFIER
               | NUMBER
               | TRUE
               | FALSE
               | LPAREN Expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_error(p):
    print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}'")

# Add this rule at the end of your lexer definition
def t_SPACE(t):
    r'[\s\t]+'
    pass  # No return value, so we skip spaces and tabs

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Test the parser with an R while loop code
code = '''while (x <= 5) {
  x <- x + 1
  while (y <= 4) {
  y <- y - 1
  }
}
'''

parsed = parser.parse(code)
print(parsed)
