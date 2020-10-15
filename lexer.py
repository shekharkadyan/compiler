## Code Begins

import ply.lex as lex
import sys

reserved = {
        'alpha':'ALPHA',
	'array':'ARRAY',
	'begin':'BEGIN',
	'boolean':'BOOLEAN_KEYWORD',
	'comment':'COMMENT',
	'continue':'CONTINUE',
	'direct':'DIRECT',
	'do':'DO',
	'double':'DOUBLE',
	'else':'ELSE',
	'end':'END',
	'event':'EVENT',
	'false':'FALSE',
	'file':'FILE',
	'for':'FOR',
	'format':'FORMAT',
	'go':'GO',
	'if':'IF',
	'integer':'INTEGER',
	'label':'LABEL',
	'list':'LIST',
	'long':'LONG',
	'own':'OWN',
	'pointer':'POINTER',
	'procedure':'PROCEDURE',
	'real':'REAL_KEYWORD',
	'step':'STEP',
	'switch':'SWITCH',
	'task':'TASK',
	'then':'THEN',
	'true':'TRUE',
	'until':'UNTIL',
	'value':'VALUE',
	'while':'WHILE',
	'zip':'ZIP',
}

restricted = {
	'accept':'ACCEPT',
	'and':'AND',
	'attach':'ATTACH',
	'by':'BY',
	'call':'CALL',
	'case':'CASE',
	'cause':'CAUSE',
	'close':'CLOSE',
	'deallocate':'DEALLOCATE',
	'define':'DEFINE',
	'detach':'DETACH',
	'disable':'DISABLE',
	'display':'DISPLAY',
	'div':'DIV',
	'dump':'DUMP',
	'enable':'ENABLE',
	'eql':'EQL',
	'eqv':'EQV',
	'exchange':'EXCHANGE',
	'external':'EXTERNAL',
	'fill':'FILL',
	'forward':'FORWARD',
	'geq':'GEQ',
	'gtr':'GTR',
	'imp':'IMP',
	'in':'IN',
	'interrupt':'INTERRUPT',
	'is':'IS',
	'lb':'LB',
	'leq':'LEQ',
	'liberate':'LIBERATE',
	'line':'LINE',
	'lock':'LOCK',
	'lss':'LSS',
	'merge':'MERGE',
	'mod':'MOD',
	'monitor':'MONITOR',
	'mux':'MUX',
	'neq':'NEQ',
	'no':'NO',
	'not':'NOT',
	'on':'ON',
	'open':'OPEN',
	'or':'OR',
	'out':'OUT',
	'picture':'PICTURE',
	'process':'PROCESS',
	'procure':'PROCURE',
	'programdump':'PROGRAMDUMP',
	'rb':'RB',
	'read':'READ',
	'release':'RELEASE',
	'replace':'REPLACE',
	'reset':'RESET',
	'resize':'RESIZE',
	'rewind':'REWIND',
	'run':'RUN',
	'scan':'SCAN',
	'seek':'SEEK',
	'set':'SET',
	'skip':'SKIP',
	'sort':'SORT',
	'space':'SPACE',
	'swap':'SWAP',
	'thru':'THRU',
	'times':'TIMES_KEYWORD',
	'to':'TO',
	'wait':'WAIT',
	'when':'WHEN',
	'with':'WITH',
	'write':'WRITE',
}

# This is the list of token names.
tokens = [
    # Data types
    'INT',
    'REAL',
    'STRING',
    'BOOLEAN',

    # Parenthesis
    'LPAREN', 
    'RPAREN',
    'LSQUARE',
    'RSQUARE',
    
    # Arithmetic Operators
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EXPONENT',
    
    # Comparison
    'EQUALS',
    'ASSIGNMENT',
    'LESS',
    'GREATER',
    'GREATER_THAN_EQUAL_TO',
    'LESS_THAN_EQUAL_TO',
    'NOT_EQUAL',
    'IMPLICATION'
    ,
    # Identifiers
    'ID',
    
    # Delimeters and Separators
    'SEMI_COLON',
    'COLON',
    'COMMA',

    # Comments
    'comment',
    ] + list(set(reserved.values())) + list(set(restricted.values()))

# These are regular expression rules for simple tokens.
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EXPONENT = r'\^'


t_ASSIGNMENT  = r':='
t_IMPLICATION = r'=>'
t_GREATER_THAN_EQUAL_TO = r'>='
t_LESS_THAN_EQUAL_TO = r'<='
t_EQUALS = r'='
t_NOT_EQUAL = r'<>'
t_GREATER = r'>'
t_LESS = r'<'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LSQUARE  = r'\['
t_RSQUARE  = r'\]'

t_SEMI_COLON = r';'
t_COLON = r':'
t_COMMA = r','

# Boolean
def t_BOOLEAN(t):
    r'(true|false)'
    if t.value == 'true':
        t.value = True
    if t.value == 'false':
        t.value = False
    return t

# Float. This rule has to be done before the int rule.
def t_REAL(t):
    r'-?\d+((\.\d+((e\+|e-))?)|(e\+\d)|(e-\d))\d*'
    t.value = float(t.value)
    return t

# Int.
def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    if t.value > 2**31 - 1:
        if t.value > 10**35 - 1:
            t.type = 'LONG_LONG'
        else:
            t.type = 'LONG'
    return t

# Strings
def t_STRING(t):
    r'\"([^\"]|(\.))*\"'
    #r'\"[^\\"]*\"'
    escaped = 0
    str = t.value[1:-1]
    new_str = ""
    for i in range(0, len(str)):
        c = str[i]
        if escaped:
            if c == "n":
                c = "\n"
            elif c == "t":
                c = "\t"
            new_str += c
            escaped = 0
        else:
            if c == "\\":
                escaped = 1
                print 'Yo'
            else:
                new_str += c
    t.value = new_str
    return t

# Ignore comments.
def t_comment(t):
    r'(comment|COMMENT)[\s]+[^;]*;'
    t.value = (t.value)[8:]
    return t

# Track line numbers.
def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)

# LONG LONG keyword
def t_LL(t):
    r'(LONG[\s]+LONG|long[\s]+long)'
    t.type = 'LONG_LONG_KEYWORD'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if reserved.get(t.value):    # Check for reserved words
        t.type = reserved.get(t.value)
    elif restricted.get(t.value):    # Check for restricted words
        t.type = restricted.get(t.value)
    
    return t


# Read in a symbol.  This rule must be practically last since there are so few
# rules concerning what constitutes a symbol.
# These are the things that should be ignored.

t_ignore = ' \t'

# Handle errors.
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    
# Build the lexer
lexer = lex.lex()

# Sample data
data = "begin a := 4 end"
lexer.input(data)

for tok in lexer:
    print tok    
