import os
from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import base64
from pathlib import Path
from dotenv import load_dotenv

from .services.separator import create_stem_separator
from .storage.file_storage import storage

# Load environment variables
load_dotenv()

# Get configuration from environment variables
HOST = os.getenv("HOST", "0.0.0.0")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create services
stem_separator = create_stem_separator()

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "host": HOST,
        "frontend_url": FRONTEND_URL
    }

@app.post("/api/separate")
async def separate_audio(file: UploadFile):
    """
    Separate an audio file into stems using Spleeter.
    
    Args:
        file: The uploaded audio file
        
    Returns:
        Dictionary containing base64-encoded stems
    """
    # More permissive file validation
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    allowed_extensions = {'.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac'}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Save the uploaded file
        input_path = await storage.save_upload(file)
        print(f"File saved at: {input_path}")
        
        # Create a temporary directory for stems
        output_dir = storage.create_temp_dir()
        print(f"Output directory created at: {output_dir}")
        
        # Separate the audio
        stem_paths = await stem_separator.separate(input_path, output_dir)
        print(f"Stems generated: {stem_paths}")
        
        # Read and encode the stems
        stems = []
        for stem_path in stem_paths:
            with open(stem_path, 'rb') as f:
                stem_data = f.read()
                stems.append({
                    'name': Path(stem_path).stem,
                    'data': base64.b64encode(stem_data).decode()
                })
        
        # Clean up
        await storage.cleanup_files(input_path, output_dir)
        
        return JSONResponse(content={'stems': stems})
        
    except Exception as e:
        # Clean up on error
        if 'input_path' in locals():
            await storage.cleanup_files(input_path)
        if 'output_dir' in locals():
            await storage.cleanup_files(output_dir)
        raise HTTPException(status_code=500, detail=str(e))

# Create required directories
OUTPUT_DIR = Path(os.path.dirname(__file__)) / '..' / 'uploads'
OUTPUT_DIR.mkdir(exist_ok=True)

TEMP_DIR = Path(os.path.dirname(__file__)) / '..' / 'temp'
TEMP_DIR.mkdir(exist_ok=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
