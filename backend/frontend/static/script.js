document.addEventListener("DOMContentLoaded", () => {
    // Preenche os campos do formulário com a configuração atual
    fetch("/api/config")
        .then(response => response.json())
        .then(data => {
            document.getElementById("monitoring_interval").value = data.monitoring_interval;
            document.getElementById("cpu_usage").value = data.thresholds.cpu.usage;
            document.getElementById("disk_usage").value = data.thresholds.disk.usage;
            document.getElementById("ram_usage").value = data.thresholds.ram.usage;
            document.getElementById("gpu_usage").value = data.thresholds.gpu.usage;
            document.getElementById("webhook").value = data.webhook;
        })
        .catch(error => console.error("Erro ao carregar configuração:", error));
    
    const form = document.getElementById("configForm");
    form.addEventListener("submit", event => {
        event.preventDefault();
        const configData = {
            monitoring_interval: parseInt(document.getElementById("monitoring_interval").value),
            thresholds: {
                cpu: { usage: parseInt(document.getElementById("cpu_usage").value) },
                disk: { usage: parseInt(document.getElementById("disk_usage").value) },
                ram: { usage: parseInt(document.getElementById("ram_usage").value) },
                gpu: { usage: parseInt(document.getElementById("gpu_usage").value) }
            },
            webhook: document.getElementById("webhook").value
        };
        
        fetch("/api/config", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(configData)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("message").innerText = "Configuração atualizada com sucesso!";
        })
        .catch(error => {
            document.getElementById("message").innerText = "Erro ao atualizar configuração.";
            console.error("Erro:", error);
        });
    });

    // Configuração do gráfico de vCPU (média)
    const avgCtx = document.getElementById('cpuChart').getContext('2d');
    const cpuChart = new Chart(avgCtx, {
        type: 'line',
        data: {
            labels: [], // horários de coleta
            datasets: [{
                label: 'Uso Médio de CPU (%)',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Tempo'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '% de Uso'
                    },
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // Configuração do gráfico para cada vCPU
    const coreCtx = document.getElementById('cpuCoreChart').getContext('2d');
    let cpuCoreChart;
    let coresCount = 0;

    // Inicializa o gráfico de vCPUs assim que obtivermos os dados iniciais
    fetch('/api/cpu')
        .then(response => response.json())
        .then(data => {
            coresCount = data.cores_usage.length;
            const colors = [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ];
            const datasets = [];
            for (let i = 0; i < coresCount; i++) {
                datasets.push({
                    label: `CPU ${i}`,
                    data: [],
                    borderColor: colors[i % colors.length],
                    fill: false,
                    tension: 0.1
                });
            }

            cpuCoreChart = new Chart(coreCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: datasets
                },
                options: {
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Tempo'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: '% de Uso'
                            },
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        })
        .catch(err => console.error("Erro ao inicializar gráfico por vCPU:", err));

    // Atualiza ambos os gráficos a cada 5 segundos
    setInterval(() => {
        fetch('/api/cpu')
            .then(response => response.json())
            .then(data => {
                const now = new Date().toLocaleTimeString();

                // Atualiza o gráfico de uso médio
                cpuChart.data.labels.push(now);
                cpuChart.data.datasets[0].data.push(data.avg_usage);
                if (cpuChart.data.labels.length > 20) {
                    cpuChart.data.labels.shift();
                    cpuChart.data.datasets[0].data.shift();
                }
                cpuChart.update();

                // Atualiza o gráfico por vCPU, se já estiver inicializado
                if (cpuCoreChart) {
                    cpuCoreChart.data.labels.push(now);
                    data.cores_usage.forEach((usage, i) => {
                        cpuCoreChart.data.datasets[i].data.push(usage);
                        if (cpuCoreChart.data.datasets[i].data.length > 20) {
                            cpuCoreChart.data.datasets[i].data.shift();
                        }
                    });
                    if (cpuCoreChart.data.labels.length > 20) {
                        cpuCoreChart.data.labels.shift();
                    }
                    cpuCoreChart.update();
                }
            })
            .catch(err => console.error("Erro ao obter métricas de CPU:", err));
    }, 5000);
});
