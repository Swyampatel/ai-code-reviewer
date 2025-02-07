import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def save_temp_code(code):
    """Saves the user's code to a temporary file for analysis"""
    file_path = os.path.join(UPLOAD_FOLDER, "temp_code.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    return file_path

def run_flake8(file_path):
    """Runs flake8 to analyze the code for errors and style issues"""
    try:
        result = subprocess.run(
            ["flake8", file_path], capture_output=True, text=True, check=False
        )
        return result.stdout.strip() if result.stdout else "No major issues found."
    except Exception as e:
        return f"Error running flake8: {str(e)}"

def run_pylint(file_path):
    """Runs pylint to perform deeper static analysis on the code"""
    try:
        result = subprocess.run(
            ["pylint", file_path, "--disable=R,C"],  # Disabling refactor/warning messages
            capture_output=True, text=True, check=False
        )
        return result.stdout.strip().split("\n")[-10:]  # Get last 10 lines for summary
    except Exception as e:
        return f"Error running pylint: {str(e)}"

@app.route('/review', methods=['POST'])
def review():
    data = request.json
    code = data.get("code", "")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    file_path = save_temp_code(code)
    
    flake8_output = run_flake8(file_path)
    pylint_output = run_pylint(file_path)

    return jsonify({
        "flake8_review": flake8_output,
        "pylint_review": "\n".join(pylint_output)
    })

if __name__ == "__main__":
    app.run(debug=True)
