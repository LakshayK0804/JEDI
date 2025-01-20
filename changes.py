import openai
import javalang
from astComponents import *
from graph import *
from reader import *
from astComponents import *
from staticAnalysis import *
from main import *

# Configure OpenAI API key
openai.api_key = "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"

# Here we could include functions to do static analysis over the AST
"""
1. Null pointer
2. Unreachable blocks of code
3. Unused variables
4. Complex methods
5. Missing exception handling
6. Resource leaks (proper file closing ect...)
"""

java_file_path = "javaTest1.java"
with open(java_file_path, "r") as file:
    java_code = file.read()


# Flags any variables that are declared/initialized but not used
def flagUnusedVars(tree):
    # Start by getting all declared and used vars
    declaredVars = getDeclaredVars(tree)
    usedVars = getUsedVars(tree)

    # Sort list of declared/used vars in order of highest scope (most local) to lowest scope(most global)

    def scopeLen(var):
        return len(var["scope"])

    declaredVars.sort(key=scopeLen, reverse=True)
    usedVars.sort(key=scopeLen, reverse=True)

    # Need to compare both lists and return the vars that have not been used
    unUsedVars = []
    for declaredVar in declaredVars:
        used = False
        for usedVar in usedVars:
            if declaredVar["name"] == usedVar["name"]:
                if set(usedVar["scope"]).issubset(set(declaredVar["scope"])):
                    used = True
                    break

        if not used:  # if var has not been found
            # var has not been used no matching name
            unUsedVars.append(declaredVar)

    # Flagging all un used vars. (THIS WILL/COULD CHANGE DEPENDING ON LLM IMPLEMENTATION REQUIREMENTS)
    if unUsedVars:
        print("Un-Used Variables Detected . . .")
        for var in unUsedVars:
            print(
                f"Name: {var['name']}, Scope: {var['scope']}, {var['position']}")
        suggestFixesForUnusedVars(unUsedVars, tree)
    else:
        print("No Un-Used Variables Detected . . .")
    # Printing all declared/used/unused vars
    '''
    print("Pinting Declared Vars . . .")
    for varInfo in declaredVars:
        print(
            f"Name: {varInfo['name']}, Scope: {varInfo['scope']}, {varInfo['position']}")

    print()

    print("Pinting Used Vars . . .")
    for varInfo in usedVars:
        print(
            f"Name: {varInfo['name']}, Scope: {varInfo['scope']}, {varInfo['position']}")
    print()

    print("Pinting Not Used Vars . . .")
    for varInfo in unUsedVars:
        print(
            f"Name: {varInfo['name']}, Scope: {varInfo['scope']}, {varInfo['position']}")
    '''
# Function to use AI to suggest fixes for unused variables


def suggestFixesForUnusedVars(unUsedVars, tree):
    for var in unUsedVars:
        var_name = var["name"]
        var_position = var["position"]

    line = var_position.line
    column = var_position.column

    print(f"Processing variable '{var_name}' at line {line}, column {column}")
    # Prompt for AI
    prompt = f"""
    The following Java code contains an unused variable {var_name} at line {line} column {column}:
    {java_code}

    Suggest a fix for this issue. You can either:
    - Put a comment over the line that has the unused variable in it "This variable is not being used in the code"
    Provide the fixed code:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for fixing Java code issues."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.3
    )
    suggested_fix = response['choices'][0]['message']['content'].strip()

    # Print the suggested fix
    print(f"\nSuggested Fix for `{var_name}` at line {line}:\n")
    print(suggested_fix)
# Flags any lines that might have a null pointer exception


def flagNullPointer(tree):
    return


flagUnusedVars(tree)
