import sys
import ply.yacc as yacc
from Symbol_table import *

# Get the token map from the lexer.  This is required.
from lexer import tokens

global procedure_stack
global debugging

## EXPRESSION - Updated 15th april   
def p_expression(p):
    '''expression : arithmetic_expression
                  | boolean_expression
                  | designational_expression'''
    global debugging
    p[0] = Node(p[1].gettype(), p[1].getvalue(), p[1])

    
## VARIABLE DECLARATION
def p_simple_variable(p):
    'simple_variable : ID'
    ## ACCESS THE ENTRY IN SYMBOL TABLE
    global debugging
    p[0] = Node('simple-variable', p[1], [p[1]])
    
def p_subscript_expression(p):
    'subscript_expression : arithmetic_expression'
    global debugging
    if p[1].gettype() != 'integer':
        print "Error : Subscript expression is to be of 'integer' type"
    else:
        p[0] = Node(p[1].gettype(), p[1].getvalue(), p[1])
    
def p_subscript_list(p):
    '''subscript_list : subscript_expression
                      | subscript_list COMMA subscript_expression'''
    global debugging
    if len(p) == 2:
        ## Convert the integer into a list
        p[0] = Node('integer', [p[1].getvalue()], p[1])
    else:
        ## Add the next element into the list 
        p[0] = Node('integer', (p[1].getvalue()).append(p[3].getvalue()), [p[1],p[3]])
        
        
def p_array_identifier(p):
    'array_identifier : ID'
    global debugging
    ## ACCESS THE ENTRY IN SYMBOL TABLE
    p[0] = Node('array-variable', p[1], [p[1]])
    
def p_subscripted_variable(p):
    'subscripted_variable : array_identifier LSQUARE subscript_list RSQUARE'
    global debugging
        
def p_variable(p):
    '''variable : simple_variable
                | subscripted_variable'''
    global debugging
    p[0] = Node(p[1].gettype(), p[1].getvalue(), p[1])


## FUNCTION DECLARATION
def p_procedure_identifier(p):
    'procedure_identifier : ID'
    global debugging
    p[0] = Node()
    
def p_actual_parameter(p):
    '''actual_parameter : STRING
                        | expression'''
    global debugging

def p_parameter_delimiter(p):
    '''parameter_delimiter : COMMA
                           | RPAREN ID COLON LPAREN'''
    global debugging

def p_actual_parameter_list(p):
    '''actual_parameter_list : actual_parameter
                             | actual_parameter_list parameter_delimiter actual_parameter'''
    global debugging
    
def p_actual_parameter_part(p):
    '''actual_parameter_part : empty
                             | LPAREN actual_parameter_list RPAREN'''
    global debugging

def p_function_designator(p):
    '''function_designator : procedure_identifier actual_parameter_part'''
    global debugging


## ARITHMETIC EXPRESSION - UPDATED 15TH APRIL
def p_adding_operator(p):
    '''adding_operator : PLUS
                       | MINUS'''
    global debugging
    if p[1] == '+':
        p[0] = Node('binop', '+', [p[1]])
    elif p[1] == '-':
        p[0] = Node('binop', '-', [p[1]])
        
def p_multiplying_operator(p):
    '''multiplying_operator : TIMES
                            | DIVIDE'''
    global debugging
    if p[1] == '*':
        p[0] = Node('binop', '*', [p[1]])
    elif p[1] == '/':
        p[0] = Node('binop', '/', [p[1]])
    

def p_primary(p):
    '''primary : INT
               | REAL
               | LPAREN arithmetic_expression RPAREN'''
    global debugging
    ## Third rule
    if len(p) == 4:
        p[0] = Node(p[2].gettype(), p[2].getvalue(), [p[2]], [p[1],p[3]])

    ## First Rule
    elif int(p[1]) == p[1]:
        p[0] = Node('int', int(p[1]), [p[1]])

    ## Second Rule
    else:
        p[0] = Node('real', float(p[1]), [p[1]])
    
def p_factor(p):
    '''factor : primary
              | factor EXPONENT primary'''
    global debugging
    ## Second rule
    if len(p) == 4:
        if p[1].gettype() == 'int' and p[3].gettype() == 'int':
            p[0] = Node('int', (p[1].getvalue())**(p[3].getvalue()), [p[1],p[3]], p[2])
                
        elif p[1].gettype() == 'int' and p[3].gettype() == 'real':
            p[0] = Node('real', (p[1].getvalue())**(p[3].getvalue()), [p[1],p[3]], p[2])
                
        elif p[1].gettype() == 'real' and p[3].gettype() == 'int':
            p[0] = Node('real', (p[1].getvalue())**(p[3].getvalue()), [p[1],p[3]], p[2])
                
        elif p[1].gettype() == 'real' and p[3].gettype() == 'real':
            p[0] = Node('real', (p[1].getvalue())**(p[3].getvalue()), [p[1],p[3]], p[2])
                
        else:
            print "Multiplication operaion not possible on the given set of values"

    ## First Rule
    else:
        p[0] = Node(p[1].gettype(), p[1].getvalue(), [p[1]])
    
    
def p_term(p):
    '''term : factor
            | term multiplying_operator factor'''
    global debugging
    ## Second rule
    if len(p) == 4:
        if p[1].gettype() == 'int' and p[3].gettype() == 'int':
            if p[2].getvalue() == '*':
                p[0] = Node('int', p[1].getvalue()*p[3].getvalue(), [p[1],p[3]], [p[2]])
            if p[2].getvalue() == '/':
                p[0] = Node('int', (p[1].getvalue())/(p[3].getvalue()), [p[1],p[3]], [p[2]])
                
        elif p[1].gettype() == 'int' and p[3].gettype() == 'real':
            if p[2].getvalue() == '*':
                p[0] = Node('real', p[1].getvalue()*p[3].getvalue(), [p[1],p[3]], [p[2]])
            if p[2].getvalue() == '/':
                p[0] = Node('real', (p[1].getvalue())/(p[3].getvalue()), [p[1],p[3]], [p[2]])
                
        elif p[1].gettype() == 'real' and p[3].gettype() == 'int':
            if p[2].getvalue() == '*':
                p[0] = Node('real', p[1].getvalue()*p[3].getvalue(), [p[1],p[3]], [p[2]])
            if p[2].getvalue() == '/':
                p[0] = Node('real', (p[1].getvalue())/(p[3].getvalue()), [p[1],p[3]], [p[2]])
                
        elif p[1].gettype() == 'real' and p[3].gettype() == 'real':
            if p[2].getvalue() == '*':
                p[0] = Node('real', p[1].getvalue()*p[3].getvalue(), [p[1],p[3]], [p[2]])
            if p[2].getvalue() == '/':
                p[0] = Node('real', (p[1].getvalue())/(p[3].getvalue()), [p[1],p[3]], [p[2]])
                
        else:
            print "Multiplication operaion not possible on the given set of values"

    ## First Rule
    else:
        p[0] = Node(p[1].gettype(), p[1].getvalue(), [p[1]])
    
    
def p_simple_arithmetic_expression(p):
    '''simple_arithmetic_expression : term
                                    | adding_operator term
                                    | simple_arithmetic_expression adding_operator term'''
    global debugging
    ## Third rule
    if len(p) == 4:
        if p[1].gettype() == 'int' and p[3].gettype() == 'int':
            if p[2].getvalue() == '+':
                p[0] = Node('int', p[1].getvalue() + p[3].getvalue(), [p[1],p[3]], [p[2]])
            if p[2].getvalue() == '-':
                p[0] = Node('int', p[1].getvalue() - p[3].getvalue(), [p[1],p[3]], [p[2]])
                
        elif p[1].gettype() == 'int' and p[3].gettype() == 'real':
            if p[2].getvalue() == '+':
                p[0] = Node('real', p[1].getvalue() + p[3].getvalue(), [p[1],p[3]], [p[2]])
            if p[2].getvalue() == '-':
                p[0] = Node('real', p[1].getvalue() - p[3].getvalue(), [p[1],p[3]], [p[2]])
                
        elif p[1].gettype() == 'real' and p[3].gettype() == 'int':
            if p[2].getvalue() == '+':
                p[0] = Node('real', p[1].getvalue() + p[3].getvalue(), [p[1],p[3]], [p[2]])
            if p[2].getvalue() == '-':
                p[0] = Node('real', p[1].getvalue() - p[3].getvalue(), [p[1],p[3]], [p[2]])

        elif p[1].gettype() == 'real' and p[3].gettype() == 'real':
            print "Kat"
            if p[2].getvalue() == '+':
                p[0] = Node('real', p[1].getvalue() + p[3].getvalue(), [p[1],p[3]], [p[2]])
            if p[2].getvalue() == '-':
                p[0] = Node('real', p[1].getvalue() - p[3].getvalue(), [p[1],p[3]], [p[2]])

        else:
            print "Arithmetic operaion not possible on the given set of values"

    ## Second Rule
    elif len(p) == 3:
        if p[1].getvalue() == '+':
            p[0] = Node(p[1].gettype(), p[1].getvalue(), [p[1]])
        else:
            p[0] = Node(p[1].gettype(), -p[1].getvalue(), [p[1]])

    ## First Rule
    else:
        p[0] = Node(p[1].gettype(), p[1].getvalue(), [p[1]])
            
            
def p_arithmetic_expression(p):
    '''arithmetic_expression : simple_arithmetic_expression'''
    global debugging
    p[0] = Node(p[1].gettype(), p[1].getvalue(), [p[1]])
    global debugging
    if debugging:
        print "Arithmetic Expression has value: ",p[1].getvalue(),p[1].gettype() 


## BOOLEAN EXPRESSION
def p_relational_operator(p):
    '''relational_operator : EQUALS
                           | LESS
                           | LESS_THAN_EQUAL_TO
                           | GREATER
                           | GREATER_THAN_EQUAL_TO
                           | NOT_EQUAL'''
    global debugging
    if p[1] == '=':
        p[0] = Node('binop', '=', [p[1]])
    elif p[1] == '<':
        p[0] = Node('binop', '<', [p[1]])
    elif p[1] == '<=':
        p[0] = Node('binop', '<=', [p[1]])
    elif p[1] == '>':
        p[0] = Node('binop', '>', [p[1]])
    elif p[1] == '>=':
        p[0] = Node('binop', '>=', [p[1]])
    elif p[1] == '<>':
        p[0] = Node('binop', '<>', [p[1]])
    
def p_relation(p):
    '''relation : simple_arithmetic_expression relational_operator simple_arithmetic_expression'''
    global debugging            
    if len(p) == 4:
        if p[2] == '=':
            p[0] = Node('boolean', (p[1].getvalue() == p[2].getvalue()), [p[1],p[3]], [p[2]])
        elif p[2] == '<':
            p[0] = Node('boolean', (p[1].getvalue() < p[2].getvalue()), [p[1],p[3]], [p[2]])
        elif p[2] == '<=':
            p[0] = Node('boolean', (p[1].getvalue() <= p[2].getvalue()), [p[1],p[3]], [p[2]])
        elif p[2] == '>':
            p[0] = Node('boolean', (p[1].getvalue() > p[2].getvalue()), [p[1],p[3]], [p[2]])
        elif p[2] == '>=':
            p[0] = Node('boolean', (p[1].getvalue() >= p[2].getvalue()), [p[1],p[3]], [p[2]])
        else :
            p[0] = Node('boolean', (p[1].getvalue() != p[2].getvalue()), [p[1],p[3]], [p[2]])
    
def p_boolean_primary(p):
    '''boolean_primary : BOOLEAN
                       | relation
                       | LPAREN boolean_expression RPAREN'''
    global debugging
    if len(p) == 4:
        p[0] = Node('boolean', p[2].getvalue(), [p[1],p[2],p[3]])
    else:
        try:
            a = p[1].leaf
            p[0] = Node('boolean', p[1].getvalue(), [p[1]])
        except AttributeError:
            p[0] = Node('boolean', p[1], [p[1]])

def p_boolean_secondary(p):
    '''boolean_secondary : boolean_primary
                         | NOT boolean_primary'''
    global debugging
    if len(p) == 2:
        p[0] = Node('boolean', p[1].getvalue(), [p[1]])
    else:
        p[0] = Node('boolean', not p[1].getvalue(), [p[1]])
        
def p_boolean_factor(p):
    '''boolean_factor : boolean_secondary
                      | boolean_factor AND boolean_secondary'''
    global debugging
    if len(p) == 2:
        p[0] = Node('boolean', p[1].getvalue(), [p[1]])
    else:
        p[0] = Node('boolean', p[1].getvalue() and p[3].getvalue(), [p[1],p[3]],[p[2]])
        
def p_boolean_term(p):
    '''boolean_term : boolean_factor
                    | boolean_term OR boolean_factor'''
    global debugging
    if len(p) == 2:
        p[0] = Node('boolean', p[1].getvalue(), [p[1]])
    else:
        p[0] = Node('boolean', p[1].getvalue() or p[3].getvalue(), [p[1],p[3]],[p[2]])
    
def p_implication(p):
    '''implication : boolean_term
                   | implication IMPLICATION boolean_term'''
    global debugging
    if len(p) == 2:
        p[0] = Node('boolean', p[1].getvalue(), [p[1]])
    else:
        if p[1].getvalue() == True and p[3].getvalue() == False:
            p[0] = Node('boolean', False, [p[1],p[3]],[p[2]])
        else:
            p[0] = Node('boolean', True, [p[1],p[3]],[p[2]])
    

def p_simple_boolean(p):
    '''simple_boolean : implication
                      | simple_boolean EQUALS implication'''
    global debugging
    if len(p) == 2:
        p[0] = Node('boolean', p[1].getvalue(), [p[1]])
    else:
        Node('boolean', p[1].getvalue() == p[3].getvalue(), [p[1],p[3]],[p[2]])
    
def p_boolean_expression(p):
    '''boolean_expression : simple_boolean'''
    global debugging
    p[0] = Node('boolean', p[1].getvalue(), [p[1]])
    print p[0].getvalue()

## DESIGNATIONAL EXPRESSION
def p_label(p):
    ## The value of INT is greater than zero
    '''label : ID
             | INT'''
    global debugging
    
def p_switch_identifier(p):
    '''switch_identifier : ID'''
    global debugging
    
def p_switch_designator(p):
    '''switch_designator : switch_identifier LSQUARE subscript_expression RSQUARE'''
    global debugging
    
def p_simple_designational_expression(p):
    '''simple_designational_expression : label
                                       | switch_designator
                                       | LPAREN designational_expression RPAREN'''
    global debugging
    
def p_designational_expression(p):
    '''designational_expression : simple_designational_expression'''
    global debugging
    
##compound statements and blocks
def p_unlabelled_basic_statement(p):
    '''unlabelled_basic_statement : assignment_statement
                                  | go_to_statement
                                  | procedure_statement'''
    global debugging
    if debugging:
        print "Entered Unlabelled Basic Statement"

def p_basic_statement(p):
    '''basic_statement : unlabelled_basic_statement
                       | label basic_statement'''
    global debugging
    
def p_unconditional_statement(p):
    '''unconditional_statement : basic_statement
                               | compound_statement
                               | block'''
    global debugging
    
def p_statement(p):
    '''statement : unconditional_statement
                 | conditional_statement
                 | for_statement'''
    global debugging
    if debugging:
        print "Entered Statement"

def p_intermediate(p):
    '''intermediate : END
                    | SEMI_COLON compound_tail'''
    global debugging
    
def p_compound_tail(p):
    '''compound_tail : statement intermediate'''
    global debugging
    if debugging:
        print "Entered Compound tail"

def p_block_head(p): 
    '''block_head : BEGIN declaration
                  | block_head SEMI_COLON declaration'''
    global debugging
    
def p_unlabelled_compound(p):
    '''unlabelled_compound : BEGIN compound_tail'''
    global debugging
    
def p_unlabelled_block(p):
    '''unlabelled_block : block_head SEMI_COLON compound_tail'''
    global debugging
    
def p_compound_statement(p):
    '''compound_statement : unlabelled_compound
                          | label COLON compound_statement'''
    global debugging
    if debugging:
        print "Entered Compound Statement"
        
def p_block(p):
    '''block : unlabelled_block
             | label COLON block'''
    global debugging
    if debugging:
        print "Entered block"
    
def p_program(p):
    '''program : block
               | compound_statement'''
    global debugging
    if debugging:
        print "Entered program"
        
##assignment statements
def p_left_part(p):
    '''left_part : variable ASSIGNMENT'''
    ##if entry not found in Symbol-table:
    ##    print "Error !! Variable cannot be assigned as it has not been intialised"
    global debugging
    p[0] = Node(p[1].gettype(), p[1].getvalue(), [p[1]], [p[2]])
    
def p_left_part_list(p):
    '''left_part_list : left_part
                      | left_part_list left_part'''
    global debugging
    if len(p) == 2:
        p[0] = Node(p[1].gettype(), p[1].getvalue(), [p[1]])
    else:
        p[0] = Node("left-part-list", p[1].gettype(), [p[1],p[2]])

def p_assignment_statement(p):
    '''assignment_statement : left_part_list arithmetic_expression
                            | left_part_list boolean_expression'''
    global debugging
    if debugging:
        print "Entered Assignment Statement"

##go to statements
def p_go_to_statement(p):
    '''go_to_statement : GO TO designational_expression'''
    global debugging
    
##conditional statements
def p_if_clause(p):
    '''if_clause : IF boolean_expression THEN'''
    global debugging
    
def p_if_statement(p):
    '''if_statement : if_clause unconditional_statement'''
    global debugging
    
def p_conditional_statement(p):
    '''conditional_statement : if_statement
                             | if_statement ELSE statement
                             | if_clause for_statement
                             | label COLON conditional_statement'''
    global debugging
    
##for statements
def p_for_list_element(p):
    '''for_list_element : arithmetic_expression
                        | arithmetic_expression STEP arithmetic_expression UNTIL arithmetic_expression
                        | arithmetic_expression WHILE boolean_expression'''
    global debugging
    if len(p) == 2:
        p[0] = Node("for-list-element", None, [p[1]])
    elif len(p) == 4:
        p[0] = Node("for-list-element", None, [p[1],p[3]], [p[2]])
    elif len(p) == 6:
        if p[3].getvalue() == 0:
            print "Step value can't be 0"
            p[0] = Node("Error")
        else:
            p[0] = Node("for-list-element", None, [p[1],p[3],p[5]],[p[2],p[4]])
    
    if debugging:
        print "Entered FOR-LIST-ELEMENT Statement"
        
def p_for_list(p):
    '''for_list : for_list_element
                | for_list COMMA for_list_element'''
    global debugging
    if len(p) == 2:
        p[0] = Node("for-list", None, [p[1]])
    elif len(p) == 4:
        p[0] = Node("for-list", None, [p[1],p[3]], [p[2]])
    
    if debugging:
        print "Entered FOR-LIST Statement"
    
def p_for_clause(p):
    '''for_clause : FOR variable ASSIGNMENT for_list DO'''
    global debugging
    p[0] = Node("for-clause", None, [p[2],p[4]], [p[1],p[3],p[5]])
    if len(p) == 6:
        if debugging:
            print "Entered FOR-CLAUSE Statement"
            
def p_for_statement(p):
    '''for_statement : for_clause statement
                     | label COLON for_statement'''
    global debugging
    if len(p) == 3:
        p[0] = Node("for-statement", None, [p[1],p[2]])
        if debugging:
            print "Entered FOR Statement"

    elif len(p) == 4:
        p[0] = Node("for-statement", None, [p[1],p[3]], [p[2]])
    
## Procedure statements
def p_procedure_statement(p):
    '''procedure_statement : procedure_identifier actual_parameter_part'''
    global debugging
    p[0] = Node("procedure-statement", p[2].getvalue(), [p[1],p[2]])
    
## DECLARATIONS
def p_declaration(p):
    '''declaration : type_declaration
                   | array_declaration
                   | switch_declaration
                   | procedure_declaration'''
    global debugging
    p[0] = Node("declaration", p[1].getvalue(), [p[1]])
    
## TYPE DECLARATION
def p_type_list(p):
    '''type_list : simple_variable 
		 | type_list COMMA simple_variable'''
    global debugging
    if len(p) == 2:
        ## ADD TO SYMBOL TABLE
        p[0] = Node('variable-declaration', p[-1].getvalue(), [p[1]])
        #print p[0].getvalue()
    else:
        p[0] = Node('variable-declaration', p[-1].getvalue(), [p[1],p[3]])
        #print p[0].getvalue()
        
def p_type(p):
    '''type : REAL_KEYWORD 
	    | INTEGER 
	    | BOOLEAN_KEYWORD'''
    global debugging
    p[0] = Node('type', p[1])
    
def p_local_or_own_type(p):
    '''local_or_own_type : type '''
    global debugging
    if len(p) == 2:
        p[0] = Node('local-or-own-type', p[1].getvalue(), [p[1]])
    	
def p_type_declaration(p):
    'type_declaration : local_or_own_type type_list'
    global debugging
    p[0] = Node('type-declaration', p[1].getvalue(), [p[1],p[2]])
	

## ARRAY DECLARATIONS - Updated 15th april 
def p_lower_bound(p):
    'lower_bound : arithmetic_expression'
    global debugging
    if p[1].getvalue() != int(p[1].getvalue()):
        print "Error !! Lower bound of array index should be an integer"
    else:
        p[0] = Node('lower-bound', p[1].getvalue(), [p[1]])
	
def p_upper_bound(p):
    'upper_bound : arithmetic_expression'
    global debugging
    if p[1].getvalue() != int(p[1].getvalue()):
        print "Error !! Upper bound of array index should be an integer"
    else:
        p[0] = Node('upper-bound', p[1].getvalue(), [p[1]])
	
def p_bound_pair(p):
    'bound_pair : lower_bound COLON upper_bound'
    global debugging
    ## Store the lower and upper bound in a pair
    if p[3].getvalue() >= p[1].getvalue():
        ## In the value variable we are storing : [upper-bound - lower-bound, [upper-bound, lower-bound]]: We require passing (upper-bound - lower-bound) for
        ## calculation of OFFSET in the SYMBOL-TABLE
        p[0] = Node("bound-pair", [p[3].getvalue() - p[1].getvalue(), [p[1].getvalue(), p[3].getvalue()]], [p[1], p[3]], [p[2]])
    else:
        print "Upper bound should be greater than lower bound"
    
def p_bound_pair_list(p):
    '''bound_pair_list : bound_pair 
		       | bound_pair_list COMMA bound_pair'''
    global debugging
    ## Maintain the bound-pair-list as a list of list
    if len(p) == 2:
        p[0] = Node("bound-pair-list", [p[1].getvalue()[0], [p[1].getvalue()[1]]] , [p[1]])
    else:
        (p[1].getvalue()[1]).append(p[3].getvalue()[1])
        temp = (p[1].getvalue()[1])
        p[0] = Node("bound-pair-list", [(p[1].getvalue()[0])*(p[3].getvalue()[0]), temp], [p[1], p[3]], [p[2]])
        print "kat",p[0].getvalue()
        
def p_array_segment(p):
    '''array_segment : array_identifier LSQUARE bound_pair_list RSQUARE
                     | array_identifier COMMA M3 array_segment'''
    global debugging
    ## Declarations can be of the type a,b[2,4]
    if p[2] == "[":
        p[0] = Node('variable-declaration', p[-1].getvalue(), [p[1], p[3]], [p[2], p[4]])
        #print p[0].getvalue()
    else:
        p[0] = Node('variable-declaration', p[-1].getvalue(), [p[1], p[4]], [p[2], p[3]])
        #print p[0].getvalue()
    	
def p_array_list(p):
    '''array_list : array_segment
                  | array_list COMMA M4 array_segment'''
    global debugging
    if len(p) == 2:
        p[0] = Node('array_list', p[-1].getvalue(), [p[1]])
    else:
        p[0] = Node('array_list', p[-1].getvalue(), [p[1], p[4]], [p[2], p[3]])
	
def p_array_declaration(p):
    '''array_declaration : ARRAY M1 array_list 
			 | local_or_own_type ARRAY M2 array_list'''
    global debugging
    ## Implicit type of declaration is 'real'	
    if len(p) == 4:
        p[0] = Node('array_declaration', None, [p[3]], [p[1], p[2]])
    else:
        p[0] = Node('array_declaration', None, [p[4]], [p[1], p[2], p[3]])

def p_M1(p):
    'M1 : empty'
    global debugging
    p[0] = Node('Marker', 'real', [p[1]])
    if debugging:
        print "M1",p[0].getvalue()

def p_M2(p):
    'M2 : empty'
    global debugging
    p[0] = Node('Marker', p[-2].getvalue(), [p[1]])
    if debugging:
        print "M2",p[0].getvalue()
    
def p_M3(p):
    'M3 : empty'
    global debugging
    p[0] = Node('Marker', p[-3].getvalue(), [p[1]])
    if debugging:
        print "M3",p[0].getvalue(),p.lineno(0)

def p_M4(p):
    'M4 : empty'
    global debugging
    p[0] = Node('Marker', p[-3].getvalue(), [p[1]])
    if debugging:
        print "M4",p[0].getvalue(),p.lineno(0)
    
## SWITCH DECLARATION
def p_switch_list(p):
    '''switch_list : designational_expression
		   | switch_list COMMA designational_expression'''
    global debugging
    
def p_switch_declaration(p):
    'switch_declaration : SWITCH switch_identifier ASSIGNMENT switch_list'
    global debugging
    
## PROCEDURE DECLARATIONS
def p_formal_parameter(p) :
    'formal_parameter : ID'
    global debugging
    
def p_formal_parameter_list(p) :
    '''formal_parameter_list : formal_parameter 
		             | formal_parameter_list parameter_delimiter formal_parameter'''
    global debugging
    
def p_formal_parameter_part(p) :
    '''formal_parameter_part : empty 
			     | LPAREN formal_parameter_list RPAREN'''
    global debugging
    
def p_identifier_list(p):
    '''identifier_list : ID 
                       | identifier_list COMMA ID'''
    global debugging
    
def p_value_part(p):
    '''value_part : VALUE identifier_list SEMI_COLON 
		  | empty'''
    global debugging
    
def p_specifier(p):
    '''specifier : STRING 
		 | type 
		 | ARRAY 
	         | type ARRAY 
		 | LABEL 
		 | SWITCH 
		 | PROCEDURE
    	         | type PROCEDURE'''
    global debugging
    
def p_specification_part(p):
    '''specification_part : specifier identifier_list SEMI_COLON
			  | specification_part specifier identifier_list SEMI_COLON'''
    global debugging
    
def p_procedure_heading(p):
    '''procedure_heading : procedure_identifier formal_parameter_part SEMI_COLON value_part specification_part
                         | procedure_identifier formal_parameter_part SEMI_COLON value_part'''
    global debugging
    
def p_procedure_body(p):
    '''procedure_body : statement'''
    global debugging
    
def p_procedure_declaration(p):
    '''procedure_declaration : type PROCEDURE procedure_heading procedure_body'''
    global debugging
    
## DUMMY STATEMENT
def p_empty(p):
    'empty : '
    global debugging
    p[0] = Node("EMPTY", '')

# Error rule for syntax errors
#def p_error(p):
#    global debugging
#    print "Syntax error in input!"

if __name__ == "__main__":
    global procedure_stack
    global debugging
   
    procedure_stack = []
    debugging = False
    
    # Build the parser
    parser = yacc.yacc(start='program')

    s = '''
           begin
           for p := 1 step 1 until 10 do s := 10
           end
        '''

    result = parser.parse(s)
    print result
