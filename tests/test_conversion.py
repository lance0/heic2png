#!/usr/bin/env python3
"""
Simple test script to verify the HEIC to PNG conversion setup.
"""

from pathlib import Path

import pillow_heif
from PIL import Image

# Register HEIF opener
pillow_heif.register_heif_opener()


def test_pil_heic_support():
    """Test if PIL can handle HEIC files (without actually having one)."""
    # Check if HEIC is in supported formats
    supported_formats = Image.EXTENSION.keys()
    heic_supported = any(".heic" in ext.lower() for ext in supported_formats)

    # Assert that HEIC support is available
    assert (
        heic_supported
    ), f"HEIC format not supported. Available formats: {list(supported_formats)}"

    # Verify that common HEIC extensions are present
    heic_extensions = [".heic", ".heics", ".heif", ".heifs"]
    found_extensions = [ext for ext in supported_formats if ext.lower() in heic_extensions]
    assert (
        len(found_extensions) > 0
    ), f"No HEIC extensions found in supported formats: {list(supported_formats)}"


if __name__ == "__main__":
    test_pil_heic_support()
