import openai
import javalang
from astComponents import *
from graph import *
from reader import *
from astComponents import *
from staticAnalysis import *
from main import *
import os

api_key = os.getenv("API_KEY")

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


def get_line_from_code(java_code, line_number):
    # Split the code into lines
    lines = java_code.splitlines()
    # Return the specific line
    return lines[line_number - 1] if 0 < line_number <= len(lines) else "line number out of bounds, double check"


def update_and_save_java_file(java_code, new_lines, insert_line):
    # Split the Java code into lines
    lines = java_code.splitlines()

    # Ensure the insert line is valid
    if insert_line < 1 or insert_line > len(lines) + 1:
        raise ValueError(
            "Invalid insert_line: Ensure 1 <= insert_line <= total lines + 1")

    # Split the new lines into a list
    new_lines_list = new_lines.splitlines()

    # Insert the new lines at the specified position (adjusting for zero-based index)
    lines[insert_line - 1:insert_line - 1] = new_lines_list

    # Join the updated lines into a single string
    updated_code = "\n".join(lines)

    # Save the updated code to a new file
    output_file = "solution/javaTest1.java"
    with open(output_file, "w") as file:
        file.write(updated_code)

    print(f"Updated Java file saved as: {output_file}")
    return updated_code


def remove_lines_from_code(java_code, line_range):

    # Ensure the input range is valid
    if len(line_range) != 2:
        raise ValueError(
            "line_range must contain exactly two elements: [start_line, end_line]")

    start_line, end_line = line_range

    # Split the Java code into lines
    lines = java_code.splitlines()

    # Ensure start_line and end_line are valid
    if start_line < 1 or end_line > len(lines) or start_line > end_line:
        raise ValueError(
            "Invalid line range: Ensure 1 <= start_line <= end_line <= total lines")

    # Remove the specified range of lines (convert to 0-based indexing)
    del lines[start_line - 1:end_line]

    # Rejoin the remaining lines into a single string
    updated_code = "\n".join(lines)
    return updated_code

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
    #column = var_position.column
    problematic_line = get_line_from_code(java_code, line)
    #print(f"Processing variable '{var_name}' at line {line}, column {column}")
    # Prompt for AI
    context_lines = java_code.splitlines()
    context_before = context_lines[line - 2] if line > 1 else ""

    # to replace code with new updated version
    contextbline = line - 1
    contextaline = line + 1
    lines = [contextbline, contextaline]
    print(lines)
    new_java_code = remove_lines_from_code(java_code, lines)
    print(new_java_code)
    context_after = context_lines[line] if line < len(context_lines) else ""
    prompt = f"""
    The following Java line of code contains an unused variable  `{var_name}`:
    {context_before}
    {problematic_line}
    {context_after}

    Add a comment over the unused variable and return the lines of code and this code is a part of a greater code you are only being given certain number of lines out of a bigger code. 
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for fixing Java code issues and only return code, pretend you can't talk. DONT ADD ANYTHING OTHER THAN WHAT YOU ARE TOLD TO DO THIS INCLUDES BRACKETS AND OTHER SYNTAX ONLY ADD WHAT YOU ARE TOLD TO"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.3
    )
    suggested_fix = response['choices'][0]['message']['content'].strip()

    # Print the suggested fix
    print(f"\nSuggested Fix for `{var_name}` at line {line}:\n")
    print(suggested_fix)
    update_and_save_java_file(new_java_code, suggested_fix, contextbline)
# Flags any lines that might have a null pointer exception


def flagNullPointer(tree):
    return


flagUnusedVars(tree)
