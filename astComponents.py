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
            scope.append("Block")
            addedScope = True

        #Check to see if a var is being declared/initialized
        if(isinstance(node, (javalang.tree.FieldDeclaration, javalang.tree.LocalVariableDeclaration))):
            #Store var name, scope, and position in declared vars
            totalScope = '.'.join(scope)
            varInfo = {
                "name": node.declarators[0].name,
                "scope": totalScope,
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

