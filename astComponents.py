#This file can be used for extracting all main AST components that might be usefull during static analysis
import javalang
from reader import readJavaFile
#func that takes java file and return an AST using javalang
def createJavaAst(filePath):
    javaString = readJavaFile(filePath)
    javaTree = javalang.parse.parse(javaString)
    return javaTree

#Function to return a list of all declared/initialized variables, includeing their scope and position
def getDeclaredVars(tree):
    declaredVars = []   #Stores all var info
    scope = []          #Stores current scope using stack datastructure
    
    def traverseTree(node):
        addedScope = False  #Checks to see if a new scope has been added to the stack
       
        #Check to see if new scope is entered (Entering class, method, or block)
        if(isinstance(node, (javalang.tree.ClassDeclaration, javalang.tree.MethodDeclaration))):
            #print("Found Class/Method decleration: ", node.name)
            #Push new scope onto stack via class/method/block name
            scope.append(node.name)
            addedScope = True
        if(isinstance(node, javalang.tree.BlockStatement)):
            #print("Found Block")
            lineNum = node.position.line   #Getting the line number of the block
            scope.append(f"Block{lineNum}")
            addedScope = True

        #Check to see if a var is being declared/initialized
        if(isinstance(node, (javalang.tree.FieldDeclaration, javalang.tree.LocalVariableDeclaration))):
            #Store var name, scope, and position in declared vars
            varInfo = {
                "name": node.declarators[0].name,
                "scope": scope[:],
                "position" : getattr(node, 'position', None)
            }
            declaredVars.append(varInfo)
                
        #If node has children, recurse
        if hasattr(node, 'children'):
            for child in node.children:
                if isinstance(child, list):     #Check to see if node has multiple children, if so recurse over all of them
                    for subchild in child:
                        if isinstance(subchild, javalang.ast.Node):
                            traverseTree(subchild)
                elif isinstance(child, javalang.ast.Node):
                    traverseTree(child)
        if addedScope:
            #print(scope)
            scope.pop()
    
    #Only pass in root node of tree
    traverseTree(tree)

    return declaredVars

#Function to return list of all used variables, including there scope and position
def getUsedVars(tree):
    usedVars = []                   #Stores all used variables
    scope = []                      #Stores current scope using stack datastructure
    
    def traverseTree(node):
        addedScope = False          #Checks to see if a new scope has been added to the stack
       
        #Check to see if new scope is entered (Entering class, method, or block)
        if(isinstance(node, (javalang.tree.ClassDeclaration))):
            #print("Found Class/Method decleration: ", node.name)
            #Push new scope onto stack via class/method/block name
            scope.append(node.name)
            addedScope = True
        if(isinstance(node, javalang.tree.BlockStatement)):
            #print("Found Block")
            lineNum = node.position.line   #Getting the line number of the block
            scope.append(f"Block{lineNum}")
            addedScope = True

        #Check to see if a var is being used, Look at MemberReference
        if(isinstance(node, (javalang.tree.MemberReference))):        
            varInfo = {
                "name": node.member,
                "scope":scope[:],
                "position" : getattr(node, 'position', None)
            }
            usedVars.append(varInfo)    #Add variable to usedVars list
            
        if(isinstance(node, (javalang.tree.MethodInvocation))):        #Need to also check for MethodInvocation node and see if there is a qualifier being used
            if(node.qualifier and node.qualifier not in {"System.out"} ):
                varInfo = {
                    "name": node.qualifier,
                    "scope": scope[:],
                    "position" : getattr(node, 'position', None)
                }
                usedVars.append(varInfo)    #Add variable to usedVars list

        #If node has children, recurse
        if hasattr(node, 'children'):
            for child in node.children:
                if isinstance(child, list):     #Check to see if node has multiple children, if so recurse over all of them
                    for subchild in child:
                        if isinstance(subchild, javalang.ast.Node):
                            traverseTree(subchild)
                elif isinstance(child, javalang.ast.Node):
                    traverseTree(child)
        if addedScope:
            #print(scope)
            scope.pop()
    
    #Only pass in root node of tree
    traverseTree(tree)

    return usedVars         #Returns all declaredVars that have not been used in the AST

#Function to return any variable with a null value
def getNullVars(tree):
    #Null value is concidered a 'literal' node with a value = none
    return