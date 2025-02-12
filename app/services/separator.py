import os
from pathlib import Path
from typing import List
from spleeter.separator import Separator

class StemSeparator:
    """Service for separating audio stems using Spleeter."""
    
    def __init__(self):
        """Initialize the Spleeter separator."""
        self.separator = Separator(
            'spleeter:4stems-16kHz',
            multiprocess=False  # More stable in container
        )
    
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
            # Convert paths to absolute paths
            input_path = str(Path(input_path).resolve())
            output_dir = str(Path(output_dir).resolve())
            
            print(f"Processing file: {input_path}")
            print(f"Output directory: {output_dir}")
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Separate the stems
            self.separator.separate_to_file(
                input_path,
                output_dir,
                filename_format='{instrument}.{codec}',
                codec='wav',
                bitrate='256k',
                duration=None  # Process entire file
            )
            
            # Expected stem files
            expected_files = ['vocals.wav', 'drums.wav', 'bass.wav', 'other.wav']
            stem_paths = []
            
            # Verify and collect output files - look directly in output directory
            for file in expected_files:
                stem_path = Path(output_dir) / file
                if not stem_path.exists():
                    raise RuntimeError(f"Missing output file: {file}")
                stem_paths.append(str(stem_path))
            
            return stem_paths
            
        except Exception as e:
            raise RuntimeError(f"Stem separation failed: {str(e)}")

# Factory function to create a stem separator instance
def create_stem_separator() -> StemSeparator:
    return StemSeparator() 