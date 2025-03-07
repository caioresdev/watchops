import psutil
from modules import config, notify

def monitor_ram():
    """
    Monitora o uso de memória RAM, retornando percentual, total, usado e disponível.
    Se o uso ultrapassar o threshold configurado, envia notificação.
    """
    cfg = config.load_config()
    ram_threshold = cfg.get("thresholds", {}).get("ram", {}).get("usage", 80)
    
    mem = psutil.virtual_memory()
    usage_percent = mem.percent

    # Conversão para GB
    total_gb = mem.total / (1024 ** 3)
    used_gb = mem.used / (1024 ** 3)
    available_gb = mem.available / (1024 ** 3)
    
    message = (
        f"⚠️ **ALERTA de Uso de RAM: {usage_percent:.1f}%**\n"
        f"📟 **Total: {mem.total}, Usado: {mem.used}, Disponível: {mem.available}.**\n"
        f"🚩 **Threshold configurado: {ram_threshold}%.**"
    )
    
    if usage_percent > ram_threshold:
        notify.send_notification(message)
    
    return {
        "total": mem.total,
        "used": mem.used,
        "available": mem.available,
        "percent": usage_percent,
        "threshold": ram_threshold,
        "total_gb": round(total_gb, 2),
        "used_gb": round(used_gb, 2),
        "available_gb": round(available_gb, 2)
    }

if __name__ == "__main__":
    metrics = monitor_ram()
    print("Métricas de RAM:", metrics)