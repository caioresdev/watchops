import psutil
import time
from config import THRESHOLDS, MONITOR_INTERVAL
from ..modules.notify import send_discord_notification

def get_ram_usage():
    """Retorna o uso de RAM em porcentagem e em bytes."""
    ram = psutil.virtual_memory()
    return ram.percent, ram.used

def monitor_ram():
    """Monitora o uso da RAM e envia notificações se o threshold for atingido."""
    while True:
        ram_percent, ram_used = get_ram_usage()
        if ram_percent > THRESHOLDS["ram"]:
            # Template da mensagem específica para RAM
            message = (
                f"⚠️ **ALERTA DE RAM** ⚠️\n"
                f"Uso da RAM atingiu {ram_percent}% (Threshold: {THRESHOLDS['ram']}%)\n"
                f"Uso em bytes: {ram_used / (1024 ** 2):.2f} MB"
            )
            # Chama a função de notificação
            send_discord_notification(message)
        time.sleep(MONITOR_INTERVAL)