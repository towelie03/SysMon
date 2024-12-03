# SysMon

SysMon is a system monitoring application that tracks CPU, memory, disk, network, and GPU usage thresholds. It provides an interface for setting and retrieving these thresholds and supports theme customization. Project for COMP-7082.

## Features

- Monitor CPU, memory, disk, network, and GPU usage
- Set thresholds for system metrics
- Customizable theme settings
- Uses FastAPI for the backend and MySQL for the database
- Dockerized for easy setup

## Prerequisites

- Python 3.9
- Docker
- Docker Compose
- Linux

## Installation

### Local Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/towelie03/SysMon.git
   cd SysMon
   ```

2. **Create a .env file with your receiver email:**
   ```sh
   echo "RECEIVER_EMAIL=YOUR_EMAIL" > .env
   ```

3. **Start the application:**
   ```sh
   docker-compose up
   ```
4. **Open your browser and navigate to:**

- Frontend: http://localhost:4173

- Backend API: http://localhost:8000/docs