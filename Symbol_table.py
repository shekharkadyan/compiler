class Node:
    def __init__(self, type = None , value = None, children = None, leaf = None, code = None):
         self.type = type
         self.value = value
         if children:
              self.children = children
         else:
              self.children = [ ]
         if leaf:
              self.leaf = leaf
         else:
              self.leaf = [ ]

    def gettype(self):
        return self.type

    def getvalue(self):
        return self.value

class ArrayEntry(object):
    def __init__(self, id = '', type='', offset = 0, size = 0):
        self.id = id
        self.type = type
        self.offset = offset
        self.size = size

class VarEntry(object):
    def __init__(self, id = '' , type = '', offset = 0, size):
        self.id = id
        self.type = type
        self.offset = offset
	self.size = size
        
#procName is the lexeme of the procedure
class ProcEntry(object):
    def __init__(self, procName='',type = [], returnType='' , pointer=None, forwardDeclaration = False):#pointer is pointer to symbol table of proc name
        self.procName = procName;
        self.type = type;
        self.returnType = returnType;
        self.pointer = pointer;
        self.forwardDeclaration = forwardDeclaration


class SymbTable(object):
    def __init__(self, parent, offset = 0):
        self.parent = parent
	self.entries = {}
	self.offset = offset

    def lookup(self, entry):
        if entry in self.entries:
            return self.entries[entry]
	elif self.parent == None:
	    return None 
        else:
            self.parent.lookup(entry)

    def insert(self, entry):
        if entry in self.entries:
            print "ERROR: Redefination of variable",entry.id
            return 0
        else:
            self.entries[entry.id] = entry
