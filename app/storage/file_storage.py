import os
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
import aiofiles
import uuid

class FileStorage:
    def __init__(self, upload_dir: str, temp_dir: str):
        """
        Initialize the file storage service.
        
        Args:
            upload_dir: Directory for storing uploaded files
            temp_dir: Directory for storing temporary files
        """
        self.upload_dir = Path(upload_dir)
        self.temp_dir = Path(temp_dir)
        
        # Create directories if they don't exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_upload(self, file: UploadFile) -> str:
        """
        Save an uploaded file and return its path.
        
        Args:
            file: The uploaded file
            
        Returns:
            Path to the saved file
        """
        # Generate a safe filename
        ext = Path(file.filename).suffix if file.filename else '.mp3'
        safe_filename = f"{uuid.uuid4()}{ext}"
        file_path = self.upload_dir / safe_filename
        
        # Save the file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        return str(file_path)
    
    def create_temp_dir(self) -> str:
        """
        Create a temporary directory for processing.
        
        Returns:
            Path to the temporary directory
        """
        temp_dir = self.temp_dir / str(uuid.uuid4())
        temp_dir.mkdir(parents=True, exist_ok=True)
        return str(temp_dir)
    
    async def cleanup_files(self, *paths: str):
        """
        Clean up files and directories.
        
        Args:
            *paths: Paths to files or directories to remove
        """
        for path in paths:
            path = Path(path)
            try:
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)
            except Exception as e:
                print(f"Error cleaning up {path}: {e}")

# Create a global instance
storage = FileStorage(
    upload_dir=os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'),
    temp_dir=os.path.join(os.path.dirname(__file__), '..', '..', 'temp')
) 