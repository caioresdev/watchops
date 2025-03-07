from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from modules import config, cpu  # Adicionamos a importação do módulo cpu

app = FastAPI()

# Configurando a pasta de arquivos estáticos e templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "frontend", "static")), name="static")

@app.get("/", response_class=HTMLResponse)
def read_index():
    index_path = os.path.join(BASE_DIR, "frontend", "templates", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/config")
def get_config():
    """Retorna a configuração atual."""
    return config.load_config()

@app.post("/api/config")
async def update_config(request: Request):
    """Atualiza a configuração com os dados enviados pelo frontend."""
    data = await request.json()
    config.update_config(data)
    return {"message": "Configuração atualizada com sucesso", "config": config.load_config()}

@app.get("/api/cpu")
def get_cpu_metrics():
    """
    Retorna as métricas de CPU.  
    O método monitor_cpu() já envia notificação se o uso médio ultrapassar o threshold.
    """
    return cpu.monitor_cpu()

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
