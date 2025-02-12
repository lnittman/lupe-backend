import os
from pathlib import Path
from typing import List
from .docker import run_spleeter_docker

class StemSeparator:
    """Service for separating audio stems using Spleeter."""
    
    async def separate(self, input_path: str, output_dir: str) -> List[str]:
        """
        Separate an audio file into stems.
        
        Args:
            input_path: Path to the input audio file
            output_dir: Directory to store the output stems
            
        Returns:
            List of paths to the generated stem files
            
        Raises:
            RuntimeError: If separation fails
        """
        try:
            # Run Spleeter in Docker
            await run_spleeter_docker(input_path, output_dir)
            
            # Get the base name of the input file without extension
            file_base_name = Path(input_path).stem
            stem_dir = Path(output_dir) / file_base_name
            
            # Expected stem files
            expected_files = ['vocals.wav', 'drums.wav', 'bass.wav', 'other.wav']
            stem_paths = []
            
            # Verify and collect output files
            for file in expected_files:
                stem_path = stem_dir / file
                if not stem_path.exists():
                    raise RuntimeError(f"Missing output file: {file}")
                stem_paths.append(str(stem_path))
            
            return stem_paths
            
        except Exception as e:
            raise RuntimeError(f"Stem separation failed: {str(e)}")

# Factory function to create a stem separator instance
def create_stem_separator() -> StemSeparator:
    return StemSeparator() 