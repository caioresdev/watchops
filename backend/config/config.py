# Configurações de Monitoramento
MONITOR_INTERVAL = 5  # Intervalo de coleta de métricas (em segundos)

# Thresholds (Limites de Alerta)
THRESHOLDS = {
    "cpu": 80,  # Uso máximo da CPU (%)
    "ram": 85,  # Uso máximo da RAM (%)
    "disk": 85,  # Uso máximo do disco (%)
    "network": {
        "upload": 1000000,  # 1 Mbps (em bytes)
        "download": 1000000,  # 1 Mbps (em bytes)
    },
    "gpu": {
        "usage": 90,  # Uso máximo da GPU (%)
        "vram": 90,  # Uso máximo da VRAM (%)
    },
    "docker": {
        "cpu": 90,  # Uso máximo de CPU por container (%)
        "ram": 90,  # Uso máximo de RAM por container (%)
    },
}

# Configurações do Discord Webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/SEU_WEBHOOK_AQUI"
DISCORD_NOTIFICATION_ENABLED = True  # Habilitar/Desabilitar notificações

# Configurações de Logs
LOG_SETTINGS = {
    "system_log_path": "/var/log/syslog",  # Caminho para logs do sistema
    "docker_logs_limit": 10,  # Número de linhas de logs a serem exibidas
}

# Configurações de API
API_SETTINGS = {
    "host": "0.0.0.0",  # Endereço do servidor da API
    "port": 5000,  # Porta do servidor da API
}