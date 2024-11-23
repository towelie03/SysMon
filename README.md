# SysMon

SysMon is a system monitoring application that tracks CPU, memory, disk, network, and GPU usage thresholds. It provides an interface for setting and retrieving these thresholds and supports theme customization. Project for COMP-7082.

## Features

- Monitor CPU, memory, disk, network, and GPU usage
- Set thresholds for system metrics
- Customizable theme settings
- Uses FastAPI for the backend and MySQL for the database
- Dockerized for easy setup

## Prerequisites

- Python 3.8+
- Docker
- Docker Compose

## Installation

### Local Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/towelie03/SysMon.git
   cd SysMon

   docker-compose up --build
   ```

