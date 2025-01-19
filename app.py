from flask import Flask, request, render_template, jsonify
import os
import shutil
from git import Repo
from graph import renderGraph
from astComponents import createJavaAst, getDeclaredVars

# Initialize Flask app
app = Flask(__name__)

# Paths to store downloaded repositories and Java files
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

        return True, f"Successfully extracted Java files to {JAVA_FILES_DIR}"
    except Exception as e:
        return False, str(e)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Handle form submission
            repo_url = request.form.get("repo_url")
            if not repo_url:
                return render_template("graph.html", error="Please provide a GitHub repository URL.")

            # Step 1: Download and extract Java files
            success, message = download_and_extract_java_files(repo_url)
            if not success:
                return render_template("graph.html", error=message)

            # Step 2: Process Java files and generate graph
            graph_url = None
            for file_name in os.listdir(JAVA_FILES_DIR):
                if file_name.endswith(".java"):
                    file_path = os.path.join(JAVA_FILES_DIR, file_name)
                    tree = createJavaAst(file_path)
                    # Generate graph and save it
                    graph_path = renderGraph(tree)
                    graph_url = graph_path.replace(
                        "static/", "")  # Convert to relative path

            # If no Java files found, show an error
            if not graph_url:
                return render_template("graph.html", error="No Java files found in the repository.")

            # Render the graph page with the graph URL
            return render_template("graph.html", graph_url=graph_url)
        except Exception as e:
            # Log the error and display an error message
            print(f"Error: {e}")
            return render_template("graph.html", error="An error occurred while processing your request. Please try again.")

    # On GET request, render the page with the form
    return render_template("graph.html")


if __name__ == "__main__":
    app.run(debug=True)
