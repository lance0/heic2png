#!/usr/bin/env python3
"""
heic2png - Batch HEIC image converter.

A command-line tool to convert HEIC images to PNG, JPG, or WebP formats.
Supports batch processing with progress tracking and parallel conversion.
"""

import argparse
import multiprocessing
import os
import sys
import time
from pathlib import Path
from typing import List, Tuple

try:
    from tqdm import tqdm

    HAS_TQDM = True
except ImportError:
    tqdm = None
    HAS_TQDM = False


def setup_image_libraries():
    """Setup PIL and pillow-heif libraries."""
    try:
        from PIL import Image
        import pillow_heif

        # Register HEIF opener with PIL
        pillow_heif.register_heif_opener()
        return Image
    except ImportError as e:
        if "PIL" in str(e):
            print("Error: PIL (Pillow) library is required. Install with: pip install Pillow")
        else:
            print(
                "Error: pillow-heif library is required for HEIC support. Install with: pip install pillow-heif"
            )
        sys.exit(1)


def find_heic_files(input_path: Path) -> List[Path]:
    """Find all HEIC files in the input directory recursively."""
    heic_files = []
    heic_files.extend(input_path.rglob("*.heic"))
    heic_files.extend(input_path.rglob("*.HEIC"))
    return sorted(heic_files)  # Sort for consistent processing


def convert_single_file(args: Tuple[Path, Path, str, str, int, bool]) -> Tuple[bool, str]:
    """
    Convert a single HEIC file to the target format.

    Returns:
        Tuple of (success: bool, message: str)
    """
    heic_file, input_path, output_dir, output_format, quality, verbose = args
    output_path = Path(output_dir)

    try:
        from PIL import Image
        import pillow_heif

        pillow_heif.register_heif_opener()
    except ImportError:
        return False, "Required libraries not available"

    # Calculate relative path from input directory
    relative_path = heic_file.relative_to(input_path)
    # Create output path with new extension
    output_file = output_path / relative_path.with_suffix(f".{output_format.lower()}")

    # Create parent directories if they don't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Skip if output file exists and is newer than input
    if output_file.exists() and output_file.stat().st_mtime > heic_file.stat().st_mtime:
        return True, f"Skipped (already up-to-date): {heic_file}"

    try:
        with Image.open(heic_file) as img:
            # Convert color mode if necessary
            if output_format.upper() in ("JPEG", "JPG") and img.mode in ("RGBA", "LA", "P"):
                # Create white background for transparent images when converting to JPG
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background
            elif img.mode not in ("RGB", "RGBA") and output_format.upper() == "PNG":
                img = img.convert("RGB")

            # Save with appropriate format and quality
            save_kwargs = {}
            if output_format.upper() in ("JPEG", "JPG", "WEBP"):
                save_kwargs["quality"] = quality
                if img.mode == "RGBA" and output_format.upper() == "WEBP":
                    save_kwargs["lossless"] = True
                elif img.mode == "RGBA":
                    img = img.convert("RGB")  # WebP can handle RGBA, but JPG cannot

            img.save(output_file, output_format.upper(), **save_kwargs)

            if verbose:
                return True, f"✓ Converted: {heic_file} -> {output_file}"
            else:
                return True, ""

    except Exception as e:
        return False, f"✗ Error converting {heic_file}: {e}"


def convert_heic_files(
    input_dir: str,
    output_dir: str,
    output_format: str = "PNG",
    quality: int = 85,
    verbose: bool = True,
    parallel: bool = True,
    dry_run: bool = False,
) -> None:
    """
    Convert all HEIC files in input_dir to the specified format.

    Args:
        input_dir: Path to directory containing HEIC files
        output_dir: Path to output directory
        output_format: Output format ('PNG', 'JPG', 'WEBP')
        quality: Quality for lossy formats (1-100)
        verbose: Whether to show detailed progress
        parallel: Whether to use parallel processing
        dry_run: If True, only show what would be converted
    """
    Image = setup_image_libraries()

    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Validate input directory
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist")
        sys.exit(1)

    if not input_path.is_dir():
        print(f"Error: '{input_dir}' is not a directory")
        sys.exit(1)

    # Create output directory if it doesn't exist
    if not dry_run:
        output_path.mkdir(parents=True, exist_ok=True)

    # Find HEIC files
    heic_files = find_heic_files(input_path)

    if not heic_files:
        print(f"No HEIC files found in '{input_dir}'")
        return

    if dry_run:
        print(f"DRY RUN: Would convert {len(heic_files)} HEIC file(s) to {output_format}")
        for heic_file in heic_files[:5]:  # Show first 5
            relative_path = heic_file.relative_to(input_path)
            output_file = output_path / relative_path.with_suffix(f".{output_format.lower()}")
            print(f"  {heic_file} -> {output_file}")
        if len(heic_files) > 5:
            print(f"  ... and {len(heic_files) - 5} more files")
        return

    print(f"Converting {len(heic_files)} HEIC file(s) to {output_format}...")

    start_time = time.time()

    # Prepare arguments for conversion
    conversion_args = [
        (heic_file, input_path, str(output_path), output_format, quality, verbose)
        for heic_file in heic_files
    ]

    results = []
    if parallel and len(heic_files) > 1:
        # Use multiprocessing for parallel conversion
        cpu_count = min(multiprocessing.cpu_count(), len(heic_files))
        print(f"Using {cpu_count} parallel processes...")

        with multiprocessing.Pool(processes=cpu_count) as pool:
            if HAS_TQDM and not verbose:
                # Use progress bar for parallel processing
                results = list(
                    tqdm(  # type: ignore
                        pool.imap(convert_single_file, conversion_args),
                        total=len(heic_files),
                        desc="Converting",
                        unit="file",
                    )
                )
            else:
                results = list(pool.imap(convert_single_file, conversion_args))
    else:
        # Sequential processing
        if HAS_TQDM and not verbose:
            # Use progress bar for sequential processing
            results = [
                convert_single_file(args)
                for args in tqdm(conversion_args, desc="Converting", unit="file")  # type: ignore
            ]
        else:
            results = [convert_single_file(args) for args in conversion_args]

    # Process results
    converted_count = 0
    error_count = 0
    skipped_count = 0

    for success, message in results:
        if success:
            if "Skipped" in message:
                skipped_count += 1
            else:
                converted_count += 1
        else:
            error_count += 1

        if message and verbose:
            print(message)

    # Print summary
    elapsed_time = time.time() - start_time
    print(f"\nConversion complete in {elapsed_time:.1f}s:")
    print(f"  Successfully converted: {converted_count}")
    if skipped_count > 0:
        print(f"  Skipped (up-to-date): {skipped_count}")
    if error_count > 0:
        print(f"  Errors: {error_count}")

    if converted_count > 0:
        print(".1f")


def main():
    parser = argparse.ArgumentParser(
        description="Convert HEIC images to PNG, JPG, or WebP format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input_dir output_dir
  %(prog)s input_dir output_dir --format JPG --quality 90
  %(prog)s input_dir output_dir --dry-run --verbose
  %(prog)s input_dir output_dir --parallel --format WEBP
        """,
    )

    parser.add_argument("input_dir", help="Input directory containing HEIC files")
    parser.add_argument("output_dir", help="Output directory for converted files")

    parser.add_argument(
        "-f",
        "--format",
        choices=["PNG", "JPG", "WEBP"],
        default="PNG",
        help="Output format (default: PNG)",
    )
    parser.add_argument(
        "-q", "--quality", type=int, default=85, help="Quality for JPG/WebP (1-100, default: 85)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show detailed conversion progress"
    )
    parser.add_argument("--no-parallel", action="store_true", help="Disable parallel processing")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be converted without actually converting",
    )

    args = parser.parse_args()

    # Validate quality range
    if not 1 <= args.quality <= 100:
        parser.error("Quality must be between 1 and 100")

    convert_heic_files(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        output_format=args.format,
        quality=args.quality,
        verbose=args.verbose,
        parallel=not args.no_parallel,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
