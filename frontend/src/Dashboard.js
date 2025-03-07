import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Pie, Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    ArcElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    ArcElement,
    Title,
    Tooltip,
    Legend
  );  

// Componente para exibir o gráfico de Network
const NetworkChart = () => {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Pacotes Enviados',
        data: [],
        borderColor: 'rgba(0, 123, 255, 1)',
        fill: false,
        tension: 0.1,
      },
      {
        label: 'Pacotes Recebidos',
        data: [],
        borderColor: 'rgba(40, 167, 69, 1)',
        fill: false,
        tension: 0.1,
      },
    ],
  });

  useEffect(() => {
    const fetchNetwork = async () => {
      try {
        const res = await axios.get('/api/network');
        const now = new Date().toLocaleTimeString();
        setChartData(prevData => {
          const newLabels = [...prevData.labels, now];
          const newSent = [...prevData.datasets[0].data, res.data.packets_sent];
          const newRecv = [...prevData.datasets[1].data, res.data.packets_recv];
          if (newLabels.length > 20) {
            newLabels.shift();
            newSent.shift();
            newRecv.shift();
          }
          return {
            labels: newLabels,
            datasets: [
              { ...prevData.datasets[0], data: newSent },
              { ...prevData.datasets[1], data: newRecv },
            ],
          };
        });
      } catch (err) {
        console.error(err);
      }
    };

    fetchNetwork();
    const interval = setInterval(fetchNetwork, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <Line
        data={chartData}
        options={{
          scales: {
            x: { title: { display: true, text: 'Tempo' } },
            y: { title: { display: true, text: 'Pacotes' }, beginAtZero: true },
          },
        }}
      />
    </div>
  );
};

const Dashboard = () => {
  // States para dados do backend
  const [diskData, setDiskData] = useState(null);
  const [ramData, setRamData] = useState(null);
  const [cpuData, setCpuData] = useState(null);
  const [containers, setContainers] = useState([]);
  const [vCpuChartData, setVCpuChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Uso Médio de vCPU (%)',
        data: [],
        borderColor: 'rgba(75,192,192,1)',
        fill: false,
        tension: 0.1,
      },
    ],
  });

  // Polling dos endpoints
  useEffect(() => {
    const fetchDiskAndRam = async () => {
      try {
        const diskRes = await axios.get('/api/disk');
        setDiskData(diskRes.data);
        const ramRes = await axios.get('/api/ram');
        setRamData(ramRes.data);
      } catch (err) {
        console.error(err);
      }
    };

    const fetchCpu = async () => {
      try {
        const cpuRes = await axios.get('/api/cpu');
        const cpu = cpuRes.data;
        setCpuData(cpu);
        setVCpuChartData(prevData => {
          const newLabels = [...prevData.labels, new Date().toLocaleTimeString()];
          const newData = [...prevData.datasets[0].data, cpu.avg_usage];
          if (newLabels.length > 20) {
            newLabels.shift();
            newData.shift();
          }
          return {
            labels: newLabels,
            datasets: [
              { ...prevData.datasets[0], data: newData },
            ],
          };
        });
      } catch (err) {
        console.error(err);
      }
    };

    const fetchContainers = async () => {
      try {
        const contRes = await axios.get('/api/containers');
        setContainers(contRes.data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchDiskAndRam();
    fetchCpu();
    fetchContainers();
    const cpuInterval = setInterval(fetchCpu, 5000);
    const diskRamInterval = setInterval(fetchDiskAndRam, 60000);
    const containersInterval = setInterval(fetchContainers, 5000);

    return () => {
      clearInterval(cpuInterval);
      clearInterval(diskRamInterval);
      clearInterval(containersInterval);
    };
  }, []);

  // Dados para gráfico de Disco (Pie Chart: Usado vs Livre)
  const diskPieData = diskData
    ? {
        labels: ['Usado (GB)', 'Livre (GB)'],
        datasets: [
          {
            data: [diskData.used_gb, diskData.free_gb],
            backgroundColor: ['#FF6384', '#36A2EB'],
          },
        ],
      }
    : null;

  // Dados para gráfico de RAM (Pie Chart: Usado vs Disponível)
  const ramPieData = ramData
    ? {
        labels: ['Usado (GB)', 'Disponível (GB)'],
        datasets: [
          {
            data: [ramData.used_gb, ramData.available_gb],
            backgroundColor: ['#FFCE56', '#4BC0C0'],
          },
        ],
      }
    : null;

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dashboard de Monitoramento</h1>
      
      <div style={{ display: 'flex', justifyContent: 'space-around', marginBottom: '40px' }}>
        {diskPieData && (
          <div>
            <h2>Uso de Disco</h2>
            <Pie data={diskPieData} />
            <p>Total: {diskData.total_gb} GB</p>
          </div>
        )}
        {ramPieData && (
          <div>
            <h2>Uso de RAM</h2>
            <Pie data={ramPieData} />
            <p>Total: {ramData.total_gb} GB</p>
          </div>
        )}
      </div>

      <div style={{ marginBottom: '40px' }}>
        <h2>Uso de vCPU</h2>
        <Line
          data={vCpuChartData}
          options={{
            scales: {
              x: { title: { display: true, text: 'Tempo' } },
              y: { title: { display: true, text: '% de Uso' }, beginAtZero: true, max: 100 },
            },
          }}
        />
      </div>

      <div style={{ marginBottom: '40px' }}>
        <h2>Network</h2>
        <NetworkChart />
      </div>

      <div style={{ marginBottom: '40px' }}>
        <h2>Containers Docker</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse' }} border="1">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Status</th>
              <th>Uso de CPU (%)</th>
              <th>vCPU Limit</th>
              <th>RAM em Uso (MB)</th>
              <th>RAM Total (MB)</th>
              <th>Error Logs</th>
            </tr>
          </thead>
          <tbody>
            {containers.map((cont, idx) => (
              <tr key={idx}>
                <td>{cont.name}</td>
                <td>{cont.status}</td>
                <td>{cont.cpu_percent ? cont.cpu_percent.toFixed(1) : 'N/A'}</td>
                <td>{typeof cont.vcpu_limit === 'number' ? cont.vcpu_limit.toFixed(1) : cont.vcpu_limit}</td>
                <td>{cont.memory_usage ? (cont.memory_usage / (1024 * 1024)).toFixed(1) : 'N/A'}</td>
                <td>{cont.memory_limit ? (cont.memory_limit / (1024 * 1024)).toFixed(1) : 'N/A'}</td>
                <td>{cont.error_logs ? cont.error_logs.join(' | ') : 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ marginBottom: '40px' }}>
        <h2>Logs do Sistema</h2>
        <ul>
          {/* Supondo que você crie um endpoint para logs do sistema */}
          {/* Exemplo: */}
          {/* logs.map((log, i) => <li key={i}>{log}</li>) */}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
