import docker

def monitor_docker():
    """
    Monitora os containers Docker, retornando para cada:
      - ID, nome e status
      - vCPU Limit (obtido a partir de 'NanoCpus')
      - Se estiver rodando, estatísticas de CPU e memória
      - Últimas 5 linhas de logs e os 5 últimos logs contendo "error"
    """
    client = docker.from_env()
    containers = client.containers.list(all=True)
    containers_info = []
    
    for container in containers:
        info = {
            "id": container.id,
            "name": container.name,
            "status": container.status,
        }
        # Obtém o limite de vCPUs (NanoCpus em nanoCPUs, divida por 1e9)
        try:
            attrs = container.attrs
            nano_cpus = attrs['HostConfig'].get('NanoCpus', 0)
            vcpu_limit = nano_cpus / 1e9 if nano_cpus else "Unlimited"
        except Exception:
            vcpu_limit = "N/A"
        info["vcpu_limit"] = vcpu_limit

        if container.status == "running":
            try:
                stats = container.stats(stream=False)
                try:
                    cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
                    system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]
                    if system_delta > 0.0:
                        cpu_percent = (cpu_delta / system_delta) * len(stats["cpu_stats"]["cpu_usage"].get("percpu_usage", [])) * 100.0
                    else:
                        cpu_percent = 0.0
                except Exception:
                    cpu_percent = None
                
                memory_usage = stats["memory_stats"].get("usage", None)
                memory_limit = stats["memory_stats"].get("limit", None)
                
                info["cpu_percent"] = cpu_percent
                info["memory_usage"] = memory_usage
                info["memory_limit"] = memory_limit
            except Exception:
                info["cpu_percent"] = None
                info["memory_usage"] = None
                info["memory_limit"] = None
        else:
            info["cpu_percent"] = None
            info["memory_usage"] = None
            info["memory_limit"] = None
        
        # Coleta os últimos 5 logs
        try:
            logs = container.logs(tail=5).decode('utf-8').splitlines()
        except Exception:
            logs = []
        info["logs"] = logs
        # Filtra os logs que contenham "error"
        error_logs = [line for line in logs if "error" in line.lower()]
        if len(error_logs) > 5:
            error_logs = error_logs[-5:]
        info["error_logs"] = error_logs

        containers_info.append(info)
    
    return containers_info

if __name__ == "__main__":
    import json
    print(json.dumps(monitor_docker(), indent=4))
