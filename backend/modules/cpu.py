import psutil
import time
from config import THRESHOLDS, MONITOR_INTERVAL
from ..modules.notify import send_discord_notification

def get_cpu_usage():
    """Retorna o uso de CPU de cada core."""
    return psutil.cpu_percent(interval=1, percpu=True)

def get_cpu_usage_total():
    """Retorna o uso total da CPU."""
    return psutil.cpu_percent(interval=1)

def monitor_cpu():
    """Monitora o uso da CPU e envia notificações se o threshold for atingido."""
    while True:
        cpu_usage = get_cpu_usage_total()
        if cpu_usage > THRESHOLDS["cpu"]:
            message = f"⚠️ **ALERTA DE CPU** ⚠️\nUso da CPU atingiu {cpu_usage}% (Threshold: {THRESHOLDS['cpu']}%)"
            send_discord_notification(message)
        time.sleep(MONITOR_INTERVAL)