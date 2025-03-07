import pynvml
from modules import config, notify

def monitor_gpu():
    """
    Monitora as GPUs usando NVML e retorna as métricas para cada GPU:
      - Nome
      - Utilização da GPU (%)
      - Utilização de memória (%)
      - Velocidade do fan (%)
      - Memória usada (MB) e total (MB)
    Envia notificação se a utilização da GPU ultrapassar o threshold definido.
    """
    cfg = config.load_config()
    gpu_threshold = cfg.get("thresholds", {}).get("gpu", {}).get("usage", 80)
    
    try:
        pynvml.nvmlInit()
    except Exception as e:
        return {"error": "Erro ao inicializar NVML: " + str(e)}
    
    gpu_count = pynvml.nvmlDeviceGetCount()
    gpus = []
    for i in range(gpu_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        try:
            raw_name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(raw_name, bytes):
                try:
                    name = raw_name.decode("utf-8", errors="ignore")
                except Exception:
                    name = f"GPU_{i}"
            else:
                name = raw_name
        except UnicodeDecodeError:
            name = f"GPU_{i}"
        
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        try:
            fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
        except Exception:
            fan_speed = None
        
        gpu_data = {
            "name": name,
            "gpu_util": util.gpu,
            "memory_util": util.memory,
            "fan_speed": fan_speed,
            "memory_used_mb": round(memory_info.used / (1024 * 1024), 2),
            "memory_total_mb": round(memory_info.total / (1024 * 1024), 2)
        }
        # Envia notificação se o uso de GPU ultrapassar o threshold
        if util.gpu > gpu_threshold:
            notify.send_notification(
                f"Alerta de GPU: {name} com uso de {util.gpu}% ultrapassou o threshold de {gpu_threshold}%."
            )
        gpus.append(gpu_data)
    pynvml.nvmlShutdown()
    return {"gpu_count": gpu_count, "gpus": gpus}

if __name__ == "__main__":
    print(monitor_gpu())
