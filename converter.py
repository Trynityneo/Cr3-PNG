#!/usr/bin/env python3
"""
CR3 to PNG Converter - A utility to convert Canon RAW (CR3) files to PNG format.
"""

import argparse
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple, Optional

import imageio
import rawpy
from PIL import Image, ImageFile
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('converter.log')
    ]
)
logger = logging.getLogger(__name__)

# Allow loading of truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Convert CR3 files to PNG format.')
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        default='cr3_images',
        help='Input directory containing CR3 files (default: cr3_images)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='png_images',
        help='Output directory for PNG files (default: png_images)'
    )
    
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=95,
        choices=range(1, 101),
        metavar='[1-100]',
        help='Output quality (1-100, default: 95)'
    )
    
    parser.add_argument(
        '-t', '--threads',
        type=int,
        default=4,
        help='Number of threads to use for parallel processing (default: 4)'
    )
    
    parser.add_argument(
        '--no-optimize',
        action='store_true',
        help='Disable PNG optimization (faster but larger files)'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing output files'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def setup_directories(input_dir: str, output_dir: str) -> Tuple[Path, Path]:
    """Ensure input and output directories exist."""
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    
    if not input_path.exists() or not input_path.is_dir():
        logger.error(f"Input directory does not exist: {input_path}")
        sys.exit(1)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    return input_path, output_path


def get_cr3_files(input_path: Path) -> List[Path]:
    """Get a list of CR3 files in the input directory."""
    return list(input_path.glob('*.CR3')) + list(input_path.glob('*.cr3'))


def convert_cr3_to_png(
    cr3_path: Path,
    output_path: Path,
    quality: int = 95,
    optimize: bool = True,
    overwrite: bool = False
) -> Tuple[bool, str]:
    """Convert a single CR3 file to PNG."""
    png_path = output_path / f"{cr3_path.stem}.png"
    
    # Skip if output exists and not overwriting
    if png_path.exists() and not overwrite:
        return False, f"Skipped (exists): {cr3_path.name}"
    
    try:
        # Read and process CR3 file
        with rawpy.imread(str(cr3_path)) as raw:
            rgb = raw.postprocess()
        
        # Save as PNG
        imageio.imsave(png_path, rgb)
        
        # Optimize if requested
        if optimize:
            with Image.open(png_path) as img:
                img.save(
                    png_path,
                    'PNG',
                    optimize=True,
                    quality=quality,
                    compress_level=9
                )
        
        return True, f"Converted: {cr3_path.name} -> {png_path.name}"
    
    except Exception as e:
        logger.error(f"Error converting {cr3_path.name}: {str(e)}")
        return False, f"Failed: {cr3_path.name} - {str(e)}"


def print_banner():
    """Print the application banner."""
    print("""
  ____  ____  ____     _        ____  _   _  ____ 
 / ___|/ ___||  _ \   | |_ ___ |  _ \| \ | |/ ___|
| |   | |    | |_) |  | __/ _ \| |_) |  \| | |  _ 
| |___| |___ |  _ <   | || (_) |  __/| |\  | |_| |
 \____\\____||_| \_\   \__\___/|_|   |_| \_|\____|
                                                  
""")
    print("CR3 to PNG Converter - Designed by VishnuXrobot\n")


def main():
    """Main function to handle the conversion process."""
    print_banner()
    args = parse_arguments()
    
    # Set log level based on verbosity
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    
    # Setup directories
    input_path, output_path = setup_directories(args.input, args.output)
    logger.info(f"Input directory: {input_path}")
    logger.info(f"Output directory: {output_path}")
    
    # Get CR3 files
    cr3_files = get_cr3_files(input_path)
    
    if not cr3_files:
        logger.warning(f"No CR3 files found in {input_path}")
        return
    
    logger.info(f"Found {len(cr3_files)} CR3 file(s) to process")
    
    # Process files
    successful = 0
    failed = 0
    skipped = 0
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        # Create a future for each file
        future_to_file = {
            executor.submit(
                convert_cr3_to_png,
                cr3_file,
                output_path,
                args.quality,
                not args.no_optimize,
                args.overwrite
            ): cr3_file for cr3_file in cr3_files
        }
        
        # Process results as they complete
        with tqdm(total=len(cr3_files), desc="Converting", unit="file") as pbar:
            for future in as_completed(future_to_file):
                cr3_file = future_to_file[future]
                try:
                    success, message = future.result()
                    logger.debug(message)
                    if success:
                        successful += 1
                    elif "Skipped" in message:
                        skipped += 1
                    else:
                        failed += 1
                except Exception as e:
                    logger.error(f"Error processing {cr3_file.name}: {str(e)}")
                    failed += 1
                pbar.update(1)
    
    # Print summary
    print("\nConversion Summary:")
    print(f"  - Successful: {successful}")
    print(f"  - Skipped: {skipped}")
    print(f"  - Failed: {failed}")
    
    if failed > 0:
        logger.warning("Some files failed to convert. Check the log for details.")
    
    logger.info("Conversion complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Conversion cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {str(e)}", exc_info=True)
        sys.exit(1)
