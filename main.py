from graph import * 
from reader import *
from astComponents import *

#Creating AST tree from java file
tree = createJavaAst("javaTest1.java")

#display graph to the screen
renderGraph(tree)

#Display all nodes in tree to terminal
#printJavaTree(tree)

#Retrieving all declared vars in AST including their name, scope, and position
declaredVars = getDeclaredVars(tree)

#Printing all declared vars in AST
for varInfo in declaredVars:
    print(f"Name: {varInfo['name']}, Scope: {varInfo['scope']}, Position: {varInfo['position']}")