#!/usr/bin/env python3
"""
Simple test script to verify the HEIC to PNG conversion setup.
"""

from pathlib import Path
from PIL import Image
import pillow_heif

# Register HEIF opener
pillow_heif.register_heif_opener()

def test_pil_heic_support():
    """Test if PIL can handle HEIC files (without actually having one)."""
    print("Testing PIL HEIC support...")

    # Check if HEIC is in supported formats
    supported_formats = Image.EXTENSION.keys()
    heic_supported = any('.heic' in ext.lower() for ext in supported_formats)

    if heic_supported:
        print("✓ HEIC format is supported by PIL")
    else:
        print("✗ HEIC format is NOT supported by PIL")

    # Check registered formats
    print(f"Registered formats: {list(Image.EXTENSION.keys())}")

    return heic_supported

if __name__ == "__main__":
    test_pil_heic_support()