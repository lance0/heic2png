# heic2png

[![CI](https://github.com/lance0/heic2png/actions/workflows/ci.yml/badge.svg)](https://github.com/lance0/heic2png/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/heic2png.svg)](https://pypi.org/project/heic2png/)
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)

heic2png is a high-performance, command-line tool for batch converting HEIC images to PNG, JPG, or WebP formats. Built with parallel processing and smart optimization features, it can handle large collections of images efficiently while preserving directory structure.

Perfect for photographers, developers, and anyone working with Apple's HEIC format, heic2png offers:
• Lightning-fast parallel processing using all CPU cores
• Multiple output formats with quality control
• Progress tracking and dry-run preview
• Smart file skipping for incremental updates
• Cross-platform compatibility (Linux, macOS, Windows)
• Simple pip installation: `pip install heic2png`

Whether you're migrating photo libraries, processing batch uploads, or automating image workflows, heic2png delivers professional-grade performance with an intuitive interface. Released under the Unlicense (public domain), it's free for any use.

## Features

- 🚀 **High Performance**: Parallel processing using all CPU cores
- 🎯 **Multiple Formats**: Convert to PNG, JPG, or WebP
- 📊 **Progress Tracking**: Real-time progress bars (with tqdm)
- 🔄 **Smart Skipping**: Skip already converted files
- 🧪 **Dry Run**: Preview conversions without processing
- 🛡️ **Robust**: Comprehensive error handling and validation

## Installation

### From PyPI (Recommended)

```bash
pip install heic2png
```

### From Source

```bash
git clone https://github.com/lance0/heic2png.git
cd heic2png
pip install -e .
```

### Optional Dependencies

For progress bars:
```bash
pip install heic2png[progress]
```

For development:
```bash
pip install heic2png[dev]
```

## Requirements

- Python 3.6+
- PIL (Pillow) library
- pillow-heif library for HEIC support

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