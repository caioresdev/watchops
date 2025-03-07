import json
import os

CONFIG_FILE = "config.json"

# Configuração padrão caso o arquivo não exista
DEFAULT_CONFIG = {
    "monitoring_interval": 5,  # em segundos
    "thresholds": {
        "cpu": {"usage": 80},   # Exemplo: notificar se uso acima de 80%
        "disk": {"usage": 80},
        "ram": {"usage": 80},
        "gpu": {"usage": 80}
    },
    "webhook": ""  # URL do webhook do Discord
}

def load_config():
    """Carrega a configuração do arquivo JSON ou cria um com os valores padrão."""
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)
    return config

def save_config(config):
    """Salva a configuração no arquivo JSON."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

def update_config(new_config):
    """
    Atualiza a configuração existente com os valores do new_config e salva no arquivo.
    new_config deve ser um dicionário contendo as chaves que se deseja atualizar.
    """
    config = load_config()
    # Atualiza recursivamente as configurações existentes com os novos valores
    merge_dicts(config, new_config)
    save_config(config)

def merge_dicts(original, updates):
    """Função auxiliar para mesclar dicionários recursivamente."""
    for key, value in updates.items():
        if key in original and isinstance(original[key], dict) and isinstance(value, dict):
            merge_dicts(original[key], value)
        else:
            original[key] = value

if __name__ == "__main__":
    # Exemplo de uso:
    config = load_config()
    print("Configuração atual:", config)

    # Atualização de exemplo
    new_settings = {
        "monitoring_interval": 10,
        "thresholds": {
            "cpu": {"usage": 85}
        },
        "webhook": "https://discord.com/api/webhooks/..."
    }
    update_config(new_settings)
    print("Configuração atualizada:", load_config())
