import javalang
from astComponents import *
#Here we could include functions to do static analysis over the AST
"""
1. Null pointer
2. Unreachable blocks of code
3. Unused variables
4. Complex methods
5. Missing exception handling
6. Resource leaks (proper file closing ect...)
"""
#Flags any variables that are declared/initialized but not used
def flagUnusedVars(tree):
    #Start by getting all declared and used vars
    declaredVars = getDeclaredVars(tree)
    usedVars = getUsedVars(tree)


    #Sort list of declared/used vars in order of highest scope (most local) to lowest scope(most global)
    def scopeLen(var):
        return len(var["scope"])
    
    declaredVars.sort(key = scopeLen, reverse = True)
    usedVars.sort(key = scopeLen, reverse = True)
       
    #Need to compare both lists and return the vars that have not been used
    unUsedVars = []
    for declaredVar in declaredVars:
        used = False
        for usedVar in usedVars:
            if declaredVar["name"] == usedVar["name"]:
                if set(usedVar["scope"]).issubset(set(declaredVar["scope"])):
                    used = True
                    break

        if not used:    #if var has not been found
            unUsedVars.append(declaredVar)  #var has not been used no matching name


    #Flagging all un used vars. (THIS WILL/COULD CHANGE DEPENDING ON LLM IMPLEMENTATION REQUIREMENTS)
    if unUsedVars:
        print("Un-Used Variables Detected . . .")
        for var in unUsedVars:
            print(f"Name: {var['name']}, Scope: {var['scope']}, {var['position']}")
    else:
        print("No Un-Used Variables Detected . . .")
    #Printing all declared/used/unused vars
    
    print("Pinting Declared Vars . . .")
    for varInfo in declaredVars:
        print(f"Name: {varInfo['name']}, Scope: {varInfo['scope']}, {varInfo['position']}")
    
    print()

    print("Pinting Used Vars . . .")
    for varInfo in usedVars:
        print(f"Name: {varInfo['name']}, Scope: {varInfo['scope']}, {varInfo['position']}") 
    print()

    print("Pinting Not Used Vars . . .")
    for varInfo in unUsedVars:
        print(f"Name: {varInfo['name']}, Scope: {varInfo['scope']}, {varInfo['position']}")  
    

#Flags any lines that might have a null pointer exception
def flagNullPointer(tree):
    return
    

