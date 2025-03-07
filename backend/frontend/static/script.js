document.addEventListener("DOMContentLoaded", () => {
    // Configuração do formulário
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
            headers: { "Content-Type": "application/json" },
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

    // Inicializa gráfico de CPU (média)
    const avgCtx = document.getElementById('cpuChart').getContext('2d');
    const cpuChart = new Chart(avgCtx, {
        type: 'line',
        data: {
            labels: [],
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
                x: { title: { display: true, text: 'Tempo' } },
                y: { title: { display: true, text: '% de Uso' }, beginAtZero: true, max: 100 }
            }
        }
    });

    // Inicializa gráfico para cada vCPU
    const coreCtx = document.getElementById('cpuCoreChart').getContext('2d');
    let cpuCoreChart;
    let coresCount = 0;
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
                data: { labels: [], datasets: datasets },
                options: {
                    scales: {
                        x: { title: { display: true, text: 'Tempo' } },
                        y: { title: { display: true, text: '% de Uso' }, beginAtZero: true, max: 100 }
                    }
                }
            });
        })
        .catch(err => console.error("Erro ao inicializar gráfico por vCPU:", err));

    // Inicializa gráfico de RAM
    const ramCtx = document.getElementById('ramChart').getContext('2d');
    const ramChart = new Chart(ramCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Uso de RAM (%)',
                data: [],
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Tempo' } },
                y: { title: { display: true, text: '% de Uso' }, beginAtZero: true, max: 100 }
            }
        }
    });

    // Inicializa gráfico de Disco
    const diskCtx = document.getElementById('diskChart').getContext('2d');
    const diskChart = new Chart(diskCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Uso de Disco (%)',
                data: [],
                borderColor: 'rgba(153, 102, 255, 1)',
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Tempo' } },
                y: { title: { display: true, text: '% de Uso' }, beginAtZero: true, max: 100 }
            }
        }
    });

    // Elementos para exibir informações em GB
    const ramInfo = document.getElementById('ramInfo');
    const diskInfo = document.getElementById('diskInfo');

    // Atualiza gráficos e informações de CPU e RAM a cada 5 segundos
    function updateCpuRamMetrics() {
        const now = new Date().toLocaleTimeString();
        fetch('/api/cpu')
            .then(response => response.json())
            .then(data => {
                cpuChart.data.labels.push(now);
                cpuChart.data.datasets[0].data.push(data.avg_usage);
                if (cpuChart.data.labels.length > 20) {
                    cpuChart.data.labels.shift();
                    cpuChart.data.datasets[0].data.shift();
                }
                cpuChart.update();

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

        fetch('/api/ram')
            .then(response => response.json())
            .then(data => {
                ramChart.data.labels.push(now);
                ramChart.data.datasets[0].data.push(data.percent);
                if (ramChart.data.labels.length > 20) {
                    ramChart.data.labels.shift();
                    ramChart.data.datasets[0].data.shift();
                }
                ramChart.update();
                ramInfo.innerText = `Total: ${data.total_gb} GB | Usado: ${data.used_gb} GB | Disponível: ${data.available_gb} GB`;
            })
            .catch(err => console.error("Erro ao obter métricas de RAM:", err));
    }

    // Atualiza gráfico de Disco e informações a cada 5 minutos
    function updateDiskMetrics() {
        const now = new Date().toLocaleTimeString();
        fetch('/api/disk')
            .then(response => response.json())
            .then(data => {
                diskChart.data.labels.push(now);
                diskChart.data.datasets[0].data.push(data.percent);
                if (diskChart.data.labels.length > 20) {
                    diskChart.data.labels.shift();
                    diskChart.data.datasets[0].data.shift();
                }
                diskChart.update();
                diskInfo.innerText = `Total: ${data.total_gb} GB | Usado: ${data.used_gb} GB | Livre: ${data.free_gb} GB`;
            })
            .catch(err => console.error("Erro ao obter métricas de Disco:", err));
    }

    // Função para atualizar a tabela de containers
function updateContainersTable() {
    fetch('/api/containers')
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector("#containersTable tbody");
            tbody.innerHTML = "";
            data.forEach(container => {
                // Converte valores de memória de bytes para MB
                let ramUsage = container.memory_usage;
                let ramTotal = container.memory_limit;
                if (ramUsage !== null && typeof ramUsage === "number") {
                    ramUsage = (ramUsage / (1024 * 1024)).toFixed(1);
                } else {
                    ramUsage = "N/A";
                }
                if (ramTotal !== null && typeof ramTotal === "number") {
                    ramTotal = (ramTotal / (1024 * 1024)).toFixed(1);
                } else {
                    ramTotal = "N/A";
                }
                // Processa CPU
                let cpuUsage = container.cpu_percent;
                if (cpuUsage !== null && typeof cpuUsage === "number") {
                    cpuUsage = cpuUsage.toFixed(1);
                } else {
                    cpuUsage = "N/A";
                }
                // Obtem o vCPU Limit do container
                let vcpuLimit = container.vcpu_limit;
                if (typeof vcpuLimit === "number") {
                    vcpuLimit = vcpuLimit.toFixed(1);
                }
    
                const row = document.createElement("tr");
                row.innerHTML = `<td>${container.name}</td>
                                 <td>${container.status}</td>
                                 <td>${cpuUsage}</td>
                                 <td>${vcpuLimit}</td>
                                 <td>${ramUsage}</td>
                                 <td>${ramTotal}</td>`;
                tbody.appendChild(row);
            });
        })
        .catch(err => console.error("Erro ao obter métricas dos containers:", err));
}

    // Atualiza CPU e RAM a cada 5 segundos
    updateCpuRamMetrics();
    setInterval(updateCpuRamMetrics, 5000);

    // Atualiza Disco a cada 5 minutos
    updateDiskMetrics();
    setInterval(updateDiskMetrics, 300000);

    // Atualiza a tabela de containers a cada 5 segundos
    updateContainersTable();
    setInterval(updateContainersTable, 5000);
});
