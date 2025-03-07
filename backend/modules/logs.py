import subprocess
from modules import notify

def monitor_system_logs():
    """
    Retorna os 5 últimos logs de erro do sistema (linhas contendo "error", ignorando case)
    a partir do arquivo /var/log/syslog. Se forem encontrados logs, envia notificação.
    """
    log_file = "/var/log/syslog"
    try:
        command = f"tail -n 100 {log_file} | grep -i error | tail -n 5"
        result = subprocess.check_output(command, shell=True, universal_newlines=True)
        logs = result.strip().splitlines()
    except Exception as e:
        logs = [f"Erro ao ler logs do sistema: {str(e)}"]
    
    # Se houver logs de erro, envia notificação
    if logs and any(line.strip() for line in logs):
        notify.send_notification("Logs do Sistema: " + " | ".join(logs))
    return logs

if __name__ == "__main__":
    print(monitor_system_logs())
