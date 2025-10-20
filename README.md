# heic2png

A high-performance Python script to batch convert HEIC image files to PNG, JPG, or WebP formats with parallel processing support.

## Requirements

- Python 3.6+
- PIL (Pillow) library
- pillow-heif library for HEIC support

## Installation

```bash
pip install Pillow pillow-heif
```

## Usage

```bash
python heic2png.py [OPTIONS] <input_directory> <output_directory>
```

### Options

- `-f, --format {PNG,JPG,WEBP}`: Output format (default: PNG)
- `-q, --quality QUALITY`: Quality for JPG/WebP (1-100, default: 85)
- `-v, --verbose`: Show detailed conversion progress
- `--no-parallel`: Disable parallel processing
- `--dry-run`: Show what would be converted without actually converting
- `-h, --help`: Show help message

### Examples

Convert all HEIC files in the current directory to PNG:
```bash
python heic2png.py . ./output
```

Convert to high-quality JPG:
```bash
python heic2png.py ~/Pictures/HEIC ~/Pictures/JPG --format JPG --quality 95
```

Convert to WebP with parallel processing:
```bash
python heic2png.py input_dir output_dir --format WEBP --verbose
```

Preview what would be converted:
```bash
python heic2png.py input_dir output_dir --dry-run --verbose
```

Disable parallel processing for debugging:
```bash
python heic2png.py input_dir output_dir --no-parallel --verbose
```

## Features

- **Multiple output formats**: PNG, JPG, and WebP support
- **Parallel processing**: Automatic multi-core processing for faster conversion
- **Quality control**: Adjustable quality settings for lossy formats
- **Smart skipping**: Skips already converted files that are up-to-date
- **Recursive processing**: Handles subdirectories and preserves structure
- **Progress tracking**: Real-time conversion statistics and timing
- **Dry run mode**: Preview conversions without modifying files
- **Robust error handling**: Continues processing even if individual files fail
- **Transparency handling**: Proper conversion of images with alpha channels

## Performance

- Uses all available CPU cores by default for parallel processing
- Smart file skipping prevents unnecessary re-conversion
- Optimized memory usage with PIL's lazy loading
- Progress reporting with timing information

## Notes

- Output directories are created automatically if they don't exist
- Existing files are overwritten (unless they're newer than source)
- Transparent HEIC images are converted to RGB with white background for JPG output
- PNG and WebP formats preserve transparency when possible