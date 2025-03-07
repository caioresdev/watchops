import time
from config import THRESHOLDS, MONITOR_INTERVAL
from ..modules.notify import send_discord_notification

def get_gpu_usage():
    """Retorna o uso da GPU e VRAM."""
    # Exemplo: Usando a biblioteca `gpustat` para coletar métricas da GPU
    import gpustat
    stats = gpustat.GPUStatCollection.new_query()
    gpu_usage = stats.gpus[0].utilization
    vram_usage = stats.gpus[0].memory_used
    return gpu_usage, vram_usage

def monitor_gpu():
    """Monitora o uso da GPU e envia notificações se o threshold for atingido."""
    while True:
        gpu_usage, vram_usage = get_gpu_usage()
        if gpu_usage > THRESHOLDS["gpu"]["usage"]:
            message = (
                f"⚠️ **ALERTA DE GPU** ⚠️\n"
                f"Uso da GPU atingiu {gpu_usage}% (Threshold: {THRESHOLDS['gpu']['usage']}%)\n"
                f"Uso de VRAM: {vram_usage} MB"
            )
            send_discord_notification(message)
        time.sleep(MONITOR_INTERVAL)