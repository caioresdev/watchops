from flask import Flask, jsonify
from threading import Thread
import time
from ..modules.cpu import get_cpu_usage_total

app = Flask(__name__)

# Variável global para armazenar o uso da CPU
cpu_data = {"cpu_usage": 0}

def update_cpu_data(interval=5):
    """Atualiza os dados de uso da CPU a cada X segundos."""
    global cpu_data
    while True:
        cpu_data["cpu_usage"] = get_cpu_usage_total()
        time.sleep(interval)

@app.route('/cpu', methods=['GET'])
def cpu_usage():
    """Retorna o uso atual da CPU."""
    return jsonify(cpu_data)

if __name__ == '__main__':
    # Inicia a thread para atualizar os dados
    Thread(target=update_cpu_data, daemon=True).start()
    app.run(host=API_SETTINGS["host"], port=API_SETTINGS["port"])