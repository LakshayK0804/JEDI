from graph import * 
from reader import *
from astComponents import createJavaAst

#Creating AST tree from java file

tree = createJavaAst("C:\\Users\\marka\\OneDrive\\Desktop\\Fall 24 Research\\JEDI\\javaTest1.java")

#display graph to the screen
renderGraph(tree)

#Display all nodes in tree to terminal
showTree(tree)