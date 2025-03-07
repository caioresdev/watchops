Below is an example README in English:

---

# Server and Docker Containers Monitoring Application

## Overview

This project is a modular Python application designed to monitor an Ubuntu server along with all Docker containers running on it. The application collects various metrics such as CPU usage (per core and overall), RAM usage (both in percentage and in GB), disk usage (in percentage and GB), network I/O statistics, and GPU metrics using NVIDIA-SMI. Additionally, it gathers error logs from the system and containers, sending notifications via Discord webhooks when thresholds are exceeded or errors are detected.

The project is divided into two parts:

- **Backend:** Built with FastAPI and Uvicorn, it provides REST endpoints to retrieve monitoring data and update configurations.
- **Frontend:** Built with React, it displays charts and tables to visualize the collected metrics. **Note:** The frontend is still under development and will undergo further adjustments.

## Features

- **Server Monitoring:**
  - **CPU:** Monitor percentage usage per core and overall average.
  - **RAM:** Monitor usage in percentage and display total, used, and free memory in GB.
  - **Disk:** Monitor disk usage and display total, used, and free space in GB.
  - **Network:** Monitor network I/O (packets sent and received).
  - **GPU:** Monitor GPU metrics such as utilization, memory usage, and fan speed. Notifications are triggered if GPU usage exceeds a defined threshold.

- **Docker Containers Monitoring:**
  - Monitor container status, vCPU usage, RAM usage, and error logs.
  - Notifications for containers that are down or reporting errors.

- **Notifications:**
  - Discord notifications are sent when thresholds are exceeded or errors are detected in system logs or container logs.

## Installation and Setup

### Backend Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository/backend
   ```

2. **Create a Python virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the requirements:**

   ```bash
   pip3 install -r requirements.txt
   ```

4. **Start the backend server:**

   ```bash
   uvicorn api:app --host 0.0.0.0 --port 8000 --reload
   ```

### Frontend Setup

1. **Navigate to the frontend folder:**

   ```bash
   cd ../frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start the frontend:**

   ```bash
   npm start
   ```

   The frontend will run on [http://localhost:3000](http://localhost:3000) and communicate with the backend at [http://localhost:8000](http://localhost:8000).

## Notes

- The frontend is still under development and will receive further adjustments to improve visualizations and user experience.
- Ensure that the `config.json` file is properly configured with the desired thresholds and the Discord webhook URL.
- For GPU monitoring, the application uses NVML through the `pynvml` library; ensure that your system has the appropriate NVIDIA drivers installed.
- Docker must be installed and running, and the user executing the backend must have the necessary permissions to access Docker.

## License

This project is licensed under the MIT License.

---

Adjust the repository URL and any other details as necessary.