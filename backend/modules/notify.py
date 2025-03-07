import requests
import json
from config import DISCORD_WEBHOOK_URL, DISCORD_NOTIFICATION_ENABLED

def send_discord_notification(message):
    """
    Envia uma notificação para o Discord via webhook.
    
    :param message: Mensagem a ser enviada.
    :return: Status code da requisição ou None se as notificações estiverem desabilitadas.
    """
    if DISCORD_NOTIFICATION_ENABLED:
        data = {"content": message}
        headers = {"Content-Type": "application/json"}
        response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(data), headers=headers)
        return response.status_code
    return None