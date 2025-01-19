from graph import * 
from reader import *
from astComponents import *
from staticAnalysis import *
#Creating AST tree from java file
tree = createJavaAst("javaTest1.java")

#display graph to the screen
renderGraph(tree)

#Display all nodes in tree to terminal
#printJavaTree(tree)
 
#Method to find un used vars and flag them
flagUnusedVars(tree)