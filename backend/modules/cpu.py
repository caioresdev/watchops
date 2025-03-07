import psutil
from modules import config
from modules import notify

def monitor_cpu():
    """
    Monitora o uso de CPU por núcleo e a média geral.
    Se a média ultrapassar o threshold definido na configuração, envia uma notificação.
    Retorna um dicionário com as métricas.
    """
    cfg = config.load_config()
    cpu_threshold = cfg.get("thresholds", {}).get("cpu", {}).get("usage", 80)
    
    # Obter a porcentagem de uso por cada núcleo
    cores_usage = psutil.cpu_percent(percpu=True)
    avg_usage = sum(cores_usage) / len(cores_usage)
    
    # Preparar mensagem para notificação
    message = (
        f"⚠️ **ALERTA: Uso de CPU atingiu {avg_usage:.1f}%**\n "
        f"\n ⚡ Uso por Core = {', '.join(f'{u:.1f}%' for u in cores_usage)}. \n"
        f"\n 🚩 **Threshold configurado: {cpu_threshold}%.**"
    )
    
    if avg_usage > cpu_threshold:
        notify.send_notification(message)
    
    return {
        "cores_usage": cores_usage,
        "avg_usage": avg_usage,
        "threshold": cpu_threshold
    }

if __name__ == "__main__":
    # Testa o monitoramento de CPU
    metrics = monitor_cpu()
    print("Métricas de CPU:", metrics)
