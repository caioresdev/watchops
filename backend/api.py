from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from modules import config, cpu, ram, disk, network, containers, gpu, logs

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "tests", "static")), name="static")

@app.get("/", response_class=HTMLResponse)
def read_index():
    index_path = os.path.join(BASE_DIR, "tests", "templates", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/config")
def get_config():
    return config.load_config()

@app.post("/api/config")
async def update_config(request: Request):
    data = await request.json()
    config.update_config(data)
    return {"message": "Configuração atualizada com sucesso", "config": config.load_config()}

@app.get("/api/cpu")
def get_cpu_metrics():
    return cpu.monitor_cpu()

@app.get("/api/ram")
def get_ram_metrics():
    return ram.monitor_ram()

@app.get("/api/disk")
def get_disk_metrics():
    return disk.monitor_disk()

@app.get("/api/network")
def get_network_metrics():
    return network.monitor_network()

@app.get("/api/containers")
def get_containers_metrics():
    return containers.monitor_docker()

@app.get("/api/gpu")
def get_gpu_metrics():
    return gpu.monitor_gpu()

@app.get("/api/system_logs")
def get_system_logs():
    return logs.monitor_system_logs()

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
