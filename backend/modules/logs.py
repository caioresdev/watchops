import subprocess

def monitor_system_logs():
    """
    Retorna os 5 últimos logs de erro do sistema (linhas contendo "error", ignorando case)
    a partir do arquivo /var/log/syslog.
    """
    log_file = "/var/log/syslog"
    try:
        # Tenta ler as últimas 100 linhas, filtra as que contêm "error" e retorna as 5 últimas
        command = f"tail -n 100 {log_file} | grep -i error | tail -n 5"
        result = subprocess.check_output(command, shell=True, universal_newlines=True)
        logs = result.strip().splitlines()
    except Exception as e:
        logs = [f"Erro ao ler logs do sistema: {str(e)}"]
    return logs

if __name__ == "__main__":
    print(monitor_system_logs())
