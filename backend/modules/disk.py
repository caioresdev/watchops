import psutil
import subprocess
from modules import config, notify

def bytes_to_human(n):
    """
    Converte um valor em bytes para uma string legível (KB, MB, GB, etc.).
    """
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')
    for s in reversed(symbols):
        factor = 1024 ** symbols.index(s)
        if n >= factor:
            value = float(n) / factor
            return f"{value:.2f} {s}"
    return f"{n} B"

def monitor_disk():
    """
    Monitora o uso de disco na partição raiz ('/'), retornando percentual, total, usado e livre.
    Calcula também os valores em GB e obtém as 10 pastas com maior uso (usando -B1 para saída em bytes).
    Se o uso ultrapassar o threshold configurado, envia notificação.
    """
    cfg = config.load_config()
    disk_threshold = cfg.get("thresholds", {}).get("disk", {}).get("usage", 80)
    
    usage = psutil.disk_usage('/')
    usage_percent = usage.percent

    # Conversão para GB
    total_gb = usage.total / (1024 ** 3)
    used_gb = usage.used / (1024 ** 3)
    free_gb = usage.free / (1024 ** 3)
    
    message = (
        f"⚠️ **ALERTA de Uso de Disco: {usage_percent:.1f}%**\n"
        f"💽 **Total: {usage.total} bytes ({total_gb:.2f} GB), Usado: {usage.used} bytes ({used_gb:.2f} GB), Livre: {usage.free} bytes ({free_gb:.2f} GB).**\n"
        f"🚩 **Threshold configurado: {disk_threshold}%.**"
    )
    
    if usage_percent > disk_threshold:
        notify.send_notification(message)
    
    # Obter as 10 pastas com maior uso usando bytes (-B1) e max-depth=1
    top_folders = []
    try:
        result = subprocess.check_output(
            "timeout 10 du -BG --max-depth=1 / 2>/dev/null | sort -rn | head -n 10", 
            shell=True, 
            universal_newlines=True
        )
        for line in result.splitlines():
            parts = line.split(None, 1)
            if len(parts) == 2:
                size_bytes = int(parts[0])
                folder = parts[1]
                top_folders.append({
                    "folder": folder,
                    "size": bytes_to_human(size_bytes)
                })
    except Exception:
        top_folders = []
    
    return {
        "total": usage.total,
        "used": usage.used,
        "free": usage.free,
        "percent": usage_percent,
        "threshold": disk_threshold,
        "top_folders": top_folders,
        "total_gb": round(total_gb, 2),
        "used_gb": round(used_gb, 2),
        "free_gb": round(free_gb, 2)
    }

if __name__ == "__main__":
    metrics = monitor_disk()
    print("Métricas de Disco:", metrics)
