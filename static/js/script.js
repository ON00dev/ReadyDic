document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("generate-form");
    const messageDiv = document.getElementById("message");
    const projectType = document.getElementById("project-type");
    const subType = document.getElementById("sub-type");
    const customStructureInput = document.getElementById("custom-structure");

    const subTypeOptions = {
        "mobile": ["Java", "Kotlin"],
        "ia": ["imagem", "nlp", "visão computacional", "análise preditiva"], // Corrigido para "análise preditiva"
        "web": ["site estático", "site dinâmico", "ecommerce"]
    };

    projectType.addEventListener("change", function () {
        const selectedType = projectType.value;
        subType.innerHTML = "";
        
        if (subTypeOptions[selectedType]) {
            subType.style.display = "block";
            subType.innerHTML = `<option value="">Selecione o Subtipo</option>`;
            subTypeOptions[selectedType].forEach(option => {
                const opt = document.createElement("option");
                opt.value = option.toLowerCase(); // Removido replace(/\s/g, "-")
                opt.textContent = option;
                subType.appendChild(opt);
            });
        } else {
            subType.style.display = "none";
        }
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Impede o recarregamento da página

        const customStructure = customStructureInput.value.trim();
        if (customStructure && !validateStructure(customStructure)) {
            messageDiv.innerHTML = "<p style='color: red;'>Erro: A estrutura contém caracteres inválidos.</p>";
            return;
        }

        messageDiv.innerHTML = "<p style='color: blue;'>Gerando projeto... Aguarde.</p>";

        let formData = new FormData(form);

        fetch("/", {
            method: "POST",
            body: formData
        })
        .then(response => response.json()) // Agora espera JSON em vez de HTML
        .then(data => {
            if (data.download_url) {
                messageDiv.innerHTML = `<p style='color: green;'>${data.message}</p>
                                        <p><a href='${data.download_url}' target='_blank'>Baixar ZIP Novamente</a></p>`;
            } else {
                messageDiv.innerHTML = `<p style='color: red;'>Erro: ${data.message}</p>`;
            }
        })
        .catch(error => {
            console.error("Erro:", error);
            messageDiv.innerHTML = "<p style='color: red;'>Erro ao criar o projeto. Tente novamente.</p>";
        });
    });

    customStructureInput.addEventListener("input", function () {
        previewStructure(customStructureInput.value);
    });

    function validateStructure(input) {
        const folders = input.split(",").map(folder => folder.trim());
        const validPattern = /^[a-zA-Z0-9_/ -]+$/;
        return folders.every(folder => validPattern.test(folder));
    }

    function previewStructure(input) {
        const previewDiv = document.getElementById("preview-structure");
        previewDiv.innerHTML = "";
        
        if (!input.trim()) return;

        const folders = input.split(",").map(folder => folder.trim());
        const uniqueFolders = [...new Set(folders)];

        uniqueFolders.forEach(folder => {
            if (folder) {
                const folderElement = document.createElement("p");
                folderElement.textContent = `📁 ${folder}`;
                previewDiv.appendChild(folderElement);
            }
        });
    }
});