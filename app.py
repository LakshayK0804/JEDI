from flask import Flask, request, render_template, jsonify
import os
import subprocess
import shutil
from git import Repo
from graph import *
from reader import *
from astComponents import *

# Initialize Flask app
app = Flask(__name__)

# Path to store downloaded repositories
DOWNLOAD_DIR = "downloaded_repos"
JAVA_FILES_DIR = "java_files"

# Ensure directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(JAVA_FILES_DIR, exist_ok=True)


def download_and_extract_java_files(repo_url):
    try:
        # Clone the repository
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(DOWNLOAD_DIR, repo_name)

        # Remove old repo if it exists
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)

        Repo.clone_from(repo_url, repo_path)

        # Extract Java files
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".java"):
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(JAVA_FILES_DIR, file)
                    shutil.copy(src_path, dest_path)

        return f"Successfully extracted Java files to {JAVA_FILES_DIR}"
    except Exception as e:
        return str(e)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        repo_url = request.form.get("repo_url")
        if not repo_url:
            return jsonify({"error": "Please provide a GitHub repository URL."}), 400
        message = download_and_extract_java_files(repo_url)
        return jsonify({"message": message})
        # Creating AST tree from java file
    for files in os.listdir(JAVA_FILES_DIR):
        if files.endswith(".java"):
            file_path = os.path.join(JAVA_FILES_DIR, files)
            tree = createJavaAst(file_path)
            # display graph to the screen
            renderGraph(tree)

            # Display all nodes in tree to terminal
            # printJavaTree(tree)

            # Retrieving all declared vars in AST including their name, scope, and position
            declaredVars = getDeclaredVars(tree)

            # Printing all declared vars in AST
            for varInfo in declaredVars:
                print(
                    f"Name: {varInfo['name']}, Scope: {varInfo['scope']}, Position: {varInfo['position']}")

    return '''
        <form method="post">
            <label for="repo_url">GitHub Repo URL:</label>
            <input type="text" name="repo_url" id="repo_url" required>
            <button type="submit">Download Java Files</button>
        </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
