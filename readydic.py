import os
import shutil
import sys
import webbrowser
from flask import Flask, render_template, request
from threading import Thread

app = Flask(__name__)

def create_project_structure(project_name, project_path, project_type):
    project_root = os.path.join(project_path, project_name)
    
    if os.path.exists(project_root):
        return "Erro: O diretório do projeto já existe!"
    
    os.makedirs(project_root)
    
    structure = {
        "mobile": ["app/src/main/java", "app/src/main/res/layout", "app/src/main/res/values", "app/src/main/AndroidManifest.xml"],
        "web": ["src", "public", "styles", "scripts", "index.html"],
        "games": ["assets", "scripts", "scenes", "config.json"],
        "ia": ["datasets", "models", "notebooks", "requirements.txt"],
        "desktop": ["src", "bin", "config", "README.md"]
    }
    
    if project_type not in structure:
        return "Erro: Tipo de projeto desconhecido!"
    
    for item in structure[project_type]:
        path = os.path.join(project_root, item)
        if "." in item:
            open(path, "w").close()
        else:
            os.makedirs(path)
    
    return f"Projeto {project_name} criado com sucesso em {project_root}!"

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_path = request.form['project_path']
        project_type = request.form['project_type'].lower()
        message = create_project_structure(project_name, project_path, project_type)
    
    return render_template('index.html', message=message)

def start_ui():
    # Abre a interface no navegador automaticamente
    webbrowser.open("http://127.0.0.1:5556")

    # Inicia o servidor Flask
    app.run(debug=True, host='127.0.0.1', port=5556, use_reloader=False)

if __name__ == "__main__":
    # Cria uma thread para rodar o Flask
    server_thread = Thread(target=start_ui)
    server_thread.daemon = True
    server_thread.start()

    # Espera um momento para o servidor ser inicializado
    import time
    time.sleep(1)
    
    # Garantir que o navegador seja aberto após o servidor iniciar
    webbrowser.open("http://127.0.0.1:5556")
