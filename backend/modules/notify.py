import requests
from modules import config

def send_notification(message: str):
    """
    Envia uma notificação para o Discord utilizando o webhook configurado.
    """
    cfg = config.load_config()
    webhook_url = cfg.get("webhook", "")
    
    if not webhook_url:
        print("Webhook não configurado. Notificação não enviada.")
        return
    
    payload = {"content": message}
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Notificação enviada com sucesso!")
    except Exception as e:
        print("Erro ao enviar notificação:", e)