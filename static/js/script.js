document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("generate-form")
    const messageDiv = document.getElementById("message")
    const projectTypes = document.querySelectorAll(".project-type")
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault()
  
      const projectName = document.getElementById("project-name").value
      const projectPath = document.getElementById("project-path").value
      const projectType = document.getElementById("project-type").value
  
      try {
        const response = await fetch("http://127.0.0.1:5556/", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams({
            project_name: projectName,
            project_path: projectPath,
            project_type: projectType,
          }),
        })
  
        const result = await response.text()
        messageDiv.textContent = result
        messageDiv.className = result.includes("sucesso") ? "success" : "error"
      } catch (error) {
        messageDiv.textContent = "Erro ao conectar com o servidor. Por favor, tente novamente."
        messageDiv.className = "error"
      }
    })
  
    projectTypes.forEach((type) => {
      type.addEventListener("click", () => {
        const typeValue = type.getAttribute("data-type")
        document.getElementById("project-type").value = typeValue
      })
    })
  })
  
  