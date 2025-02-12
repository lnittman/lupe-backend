# Lupe Backend

Audio stem separation service built with FastAPI and Spleeter.

## Features

- Audio file upload and processing
- Stem separation using Spleeter (4 stems: vocals, drums, bass, other)
- Docker-based deployment
- Railway.app compatible

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd lupe-backend
```

2. Create and configure environment variables:
```bash
cp .env.example .env
```

3. Start the services using Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /api/health` - Health check endpoint
- `POST /api/separate` - Upload and separate audio files

## Railway Deployment

1. Push code to GitHub
2. Create new project on Railway.app
3. Connect to GitHub repository
4. Set environment variables:
   - `FRONTEND_URL` - Your frontend application URL
   - Other variables will use default values

## Environment Variables

- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)
- `FRONTEND_URL` - Frontend application URL for CORS
- `UPLOAD_DIR` - Directory for uploaded files
- `TEMP_DIR` - Directory for temporary files
- `MODEL_PATH` - Directory for Spleeter models
