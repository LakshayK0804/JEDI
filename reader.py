#Reads java file an validates them
import javalang
import graphviz

#func to read java file and return file as string, can add more checks to this later
def readJavaFile(filePath):
    with open(filePath, 'r') as file:
        return file.read()
    

#Can add more validation checks here later

#Will need some way to implement with github




