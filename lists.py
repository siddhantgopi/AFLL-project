import ply.lex as lex
import ply.yacc as yacc

# Define the list of tokens
tokens = (
    'IDENTIFIER',
    'NUMBER',
    'STRING',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'ASSIGN',
)

# Define token regular expressions
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'<-'
t_ignore = ' \t\n'

# Define token rules for IDENTIFIER, NUMBER, and STRING
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'IDENTIFIER'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"|\'[^\']*\''
    t.value = t.value[1:-1]
    return t

# Error handling for invalid characters
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Define precedence and associativity
precedence = ()

# Define the grammar rules
def p_assignment(p):
    '''assignment : IDENTIFIER ASSIGN list'''
    p[0] = ('assignment', p[1], p[3])

def p_list(p):
    '''list : LPAREN elements RPAREN'''
    p[0] = ('list', p[2])

def p_elements_single(p):
    '''elements : element'''
    p[0] = [p[1]]

def p_elements_multiple(p):
    '''elements : element COMMA elements'''
    p[0] = [p[1]] + p[3]

def p_element_identifier(p):
    '''element : IDENTIFIER'''
    p[0] = ('identifier', p[1])

def p_element_number(p):
    '''element : NUMBER'''
    p[0] = ('number', p[1])

def p_element_string(p):
    '''element : STRING'''
    p[0] = ('string', p[1])

# Error handling for syntax errors
def p_error(p):
    print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected token '{p.value}'")

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Test the parser with an example
input_code = 'my_list <- ("Alice" , 30, "New York")'
parsed = parser.parse(input_code)
print(parsed)
