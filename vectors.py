import ply.lex as lex
import ply.yacc as yacc

# Define the list of token names
tokens = (
    'LPAREN',
    'RPAREN',
    'COMMA',
    'NUMBER',
    'STRING',
    'LOGICAL',
    'IDENTIFIER',
    'C_FUNCTION',
)

# Define token regular expressions
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_STRING = r'\"[^"]*\"|\'[^\']*\''
t_LOGICAL = r'TRUE|FALSE'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

# Define a token rule for NUMBER
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Define a rule for the c() function
def t_C_FUNCTION(t):
    r'c\('
    return t

# Define error handling for invalid characters
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Define the precedence and associativity for the parser
precedence = ()

# Define the grammar rules
def p_Vector(p):
    '''Vector : C_FUNCTION VectorElements RPAREN'''
    p[0] = p[2]

def p_VectorElements_single(p):
    '''VectorElements : Element'''
    p[0] = [p[1]]

def p_VectorElements_multiple(p):
    '''VectorElements : Element COMMA VectorElements'''
    p[0] = [p[1]] + p[3]

def p_Element_number(p):
    '''Element : NUMBER'''
    p[0] = ('number', p[1])

def p_Element_string(p):
    '''Element : STRING'''
    p[0] = ('string', p[1])

def p_Element_logical(p):
    '''Element : LOGICAL'''
    p[0] = ('logical', p[1])

def p_Element_identifier(p):
    '''Element : IDENTIFIER'''
    p[0] = ('identifier', p[1])

def p_error(p):
    print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}'")

def t_SPACE(t):
    r'[\s\t]+'
    pass  # No return value, so we skip spaces and tabs

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Test the parser with an R vector expression using the c() function
code = 'c(1, "Hello", TRUE, x, 3.14)'
parsed = parser.parse(code)
print(parsed)
