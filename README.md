# Software Engineering Project

This repo contains all the files related to the Software Engineering Course - Project in IIT Madras degree in Data Science & Application.

## Setup

Get an API key from Google AI Studio for using AI features.

```bash
cd <PROJECT_NAME>/backend
mv .env.example .env
```

Now, add your keys to the `.env` file.

### Frontend: React App

Make sure `npm` is installed on your system.

```bash
cd <PROJECT_NAME>/frontend
npm install
npm run dev
```

### Backend: FastAPI Server

Make sure `uv` is installed on your system.

```bash
cd <PROJECT_NAME>/backend
uv sync
source .venv/bin/activate
uv run main.py
```
