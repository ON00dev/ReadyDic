import os
import shutil
import zipfile
import platform
from flask import Flask, render_template, request, send_file, jsonify
import re

app = Flask(__name__)

def get_default_save_path():
    if platform.system() == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "Downloads")
    elif platform.system() in ["Darwin", "Linux"]:
        return os.path.join(os.environ["HOME"], "Downloads")
    else:
        return "/sdcard/Download"

def validate_structure(custom_structure):
    valid_pattern = re.compile(r'^[a-zA-Z0-9_/ -]+$')
    valid_structure = []
    
    for folder in custom_structure.split(","):
        folder = folder.strip()
        if valid_pattern.match(folder) and folder not in valid_structure:
            valid_structure.append(folder)
    
    return valid_structure

def create_project_structure(project_name, project_path, project_type, sub_type, custom_structure):
    if not os.path.exists(project_path):
        return {"message": "Erro: O diretório especificado não existe!", "download_url": None}
    
    project_root = os.path.join(project_path, project_name)
    zip_filename = os.path.join(project_path, f"{project_name}.zip")
    
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    if os.path.exists(project_root):
        shutil.rmtree(project_root)
    
    os.makedirs(project_root, exist_ok=True)
    
    structures = {
        "mobile": {
            "java": ["app/src/main/java", "app/src/main/res", "app/src/main/AndroidManifest.xml"],
            "kotlin": ["app/src/main/kotlin", "app/src/main/res", "app/src/main/AndroidManifest.xml"]
        },
        "games": ["Assets", "Src", "Resources", "Levels", "Characters", "UI", "Audio", "Tests", "Docs", "Build"],
        "ia": {
            "imagem": ["Data", "Images", "Models", "Code", "Config", "Results"],
            "nlp": ["Data", "Text", "Models", "Code", "Config", "Results"],
            "visao": ["Data", "Images", "Video", "Models", "Code", "Config", "Results"],
            "preditiva": ["Data", "Models", "Code", "Config", "Results"]
        },
        "web": {
            "site": ["Public", "Src", "Assets", "Components", "Utils", "Tests"],
            "app": ["Public", "Src", "Assets", "Components", "Controllers", "Models", "Views", "Routes", "Utils", "Tests"],
            "ecommerce": ["Public", "Src", "Assets", "Components", "Controllers", "Models", "Views", "Routes", "Utils", "Tests", "Admin", "Api"]
        }
    }
    
    structure = structures.get(project_type, [])
    if isinstance(structure, dict):
        structure = structure.get(sub_type, [])
    
    if not structure:
        return {"message": "Erro: Tipo de projeto desconhecido!", "download_url": None}
    
    for item in structure:
        path = os.path.join(project_root, item)
        os.makedirs(path, exist_ok=True)
    
    if custom_structure:
        for item in validate_structure(custom_structure):
            path = os.path.join(project_root, item)
            os.makedirs(path, exist_ok=True)
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_root):
            for dir_name in dirs:
                folder_path = os.path.join(root, dir_name)
                zipf.write(folder_path, os.path.relpath(folder_path, project_path) + "/")
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, project_path))
    
    shutil.rmtree(project_root)
    
    return {"message": f"Projeto {project_name} criado com sucesso!", "download_url": f"/download/{project_name}"}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        project_name = request.form["project_name"]
        project_path = get_default_save_path()
        project_type = request.form["project_type"].lower()
        sub_type = request.form.get("sub_type", "").lower()
        custom_structure = request.form.get("custom_structure", "")
        result = create_project_structure(project_name, project_path, project_type, sub_type, custom_structure)
        return jsonify(result)
    
    return render_template("index.html", default_path=get_default_save_path())

@app.route("/download/<project_name>")
def download_file(project_name):
    project_path = get_default_save_path()
    zip_filename = os.path.join(project_path, f"{project_name}.zip")
    return send_file(zip_filename, as_attachment=True)

def start_ui():
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)

if __name__ == "__main__":
    start_ui()
