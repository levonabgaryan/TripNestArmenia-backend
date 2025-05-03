# Project Setup

## Requirements
Make sure you have installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry 1.8.4](https://python-poetry.org/docs/#installation)

## Setup Instructions

1. **Install dependencies**
   ```bash
   poetry install

2. **Select interpreter**
    
    Choose the interpreter from the .venv created by Poetry.

    Alternatively, activate the virtual environment manually:
    ```bash
   source .venv/bin/activate
    ```
3. **Start Docker services**
    ```bash
   docker compose up
   ```