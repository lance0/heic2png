#!/usr/bin/env python3
"""
Unit tests for heic2png.py
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
import pillow_heif

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Register HEIF opener
pillow_heif.register_heif_opener()


class TestHeic2Png(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.input_dir = Path(self.test_dir) / "input"
        self.output_dir = Path(self.test_dir) / "output"
        self.input_dir.mkdir()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.test_dir)

    def create_test_image(self, filename, size=(100, 100), color=(255, 0, 0)):
        """Create a test image file."""
        img = Image.new("RGB", size, color)
        img.save(self.input_dir / filename)

    def test_find_heic_files(self):
        """Test finding HEIC files."""
        from heic2png import find_heic_files

        # Create some test files
        (self.input_dir / "test.heic").touch()
        (self.input_dir / "other.HEIC").touch()  # Use different name to avoid case collision
        (self.input_dir / "test.jpg").touch()
        (self.input_dir / "subdir").mkdir()
        (self.input_dir / "subdir" / "nested.heic").touch()

        heic_files = find_heic_files(self.input_dir)
        self.assertEqual(len(heic_files), 3)
        self.assertTrue(all(f.suffix.lower() == ".heic" for f in heic_files))

    def test_setup_image_libraries(self):
        """Test that image libraries can be imported."""
        from heic2png import setup_image_libraries

        Image = setup_image_libraries()
        self.assertTrue(hasattr(Image, "open"))

    def test_convert_single_file_png(self):
        """Test converting a single file to PNG."""
        from heic2png import convert_single_file

        # Create a test image
        test_file = self.input_dir / "test.heic"
        self.create_test_image("test.heic")

        # Convert to PNG
        args = (test_file, self.input_dir, str(self.output_dir), "PNG", 85, True)
        success, message = convert_single_file(args)

        self.assertTrue(success)
        self.assertIn("Converted", message)

        # Check output file exists
        output_file = self.output_dir / "test.png"
        self.assertTrue(output_file.exists())

        # Verify it's a valid PNG
        with Image.open(output_file) as img:
            self.assertEqual(img.format, "PNG")
            self.assertEqual(img.size, (100, 100))


if __name__ == "__main__":
    unittest.main()
