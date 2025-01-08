#This file can be used for extracting all main AST components that might be usefull during static analysis
import javalang
from reader import readJavaFile
#func that takes java file and return an AST using javalang
def createJavaAst(filePath):
    javaString = readJavaFile(filePath)
    javaTree = javalang.parse.parse(javaString)
    return javaTree