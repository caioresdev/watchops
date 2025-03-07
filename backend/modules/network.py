import psutil

def monitor_network():
    """
    Retorna estatísticas de rede:
    - bytes enviados e recebidos
    - pacotes enviados e recebidos
    """
    net_io = psutil.net_io_counters()
    return {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv
    }

if __name__ == "__main__":
    print(monitor_network())
