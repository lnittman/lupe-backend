import os
import asyncio
from pathlib import Path

async def run_spleeter_docker(input_path: str, output_dir: str) -> None:
    """
    Run Spleeter in Docker to separate audio stems.
    
    Args:
        input_path: Path to the input audio file
        output_dir: Directory to store the output stems
    """
    # Convert paths to absolute paths
    input_path = str(Path(input_path).resolve())
    output_dir = str(Path(output_dir).resolve())
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Build the Docker command
    cmd = [
        "docker",
        "exec",
        "lupe-backend-spleeter-1",  # Container name
        "spleeter",
        "separate",
        "-p", "spleeter:4stems",  # Use 4 stems model (vocals, drums, bass, other)
        "-o", "/output",  # Output directory inside container
        f"/input/{os.path.basename(input_path)}"  # Input file inside container
    ]
    
    # Run the command
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Wait for the process to complete
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0:
        raise RuntimeError(f"Spleeter failed: {stderr.decode()}") 