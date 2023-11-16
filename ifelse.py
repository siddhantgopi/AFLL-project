import ply.lex as lex
import ply.yacc as yacc

# Define the list of token names
tokens = (
    'IF',
    'ELSE',
    'LPAREN',
    'RPAREN',
    'LBRACE',  # Define LBRACE token for '{'
    'RBRACE',  # Define RBRACE token for '}'
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
# t_IF = r'if'
# t_ELSE = r'else'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'  # Define LBRACE token
t_RBRACE = r'\}'  # Define RBRACE token
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
t_LEFT_ARROW = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

def t_IF(t):
    r'\s*if\s+'
    return t

def t_ELSE(t):
    r'\s*else\s*'
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
def p_IfStatement(p):
    '''IfStatement : IF LPAREN Expression RPAREN Block
                   | IF LPAREN Expression RPAREN Block ELSE Block'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])
    else:
        p[0] = ('if_else', p[3], p[5], p[7])

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
    '''Statement : IfStatement
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

def t_SPACE(t):
    r'[\s\t]+'
    pass  # No return value, so we skip spaces and tabs


# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Test the parser with an R if-else code
code = '''
if (x < 10) {
  y <- 20
}  
'''

parsed = parser.parse(code)
print(parsed)
