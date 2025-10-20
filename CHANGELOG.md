# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-20

### Added
- Initial release of heic2png
- Support for HEIC to PNG, JPG, and WebP conversion
- Parallel processing with automatic CPU core detection
- Progress bar support (optional, via tqdm)
- Smart file skipping for already converted files
- Dry run mode for previewing conversions
- Comprehensive CLI with argparse
- Unit tests with pytest
- CI/CD pipeline with GitHub Actions
- Python package structure with pyproject.toml
- Unlicense (public domain dedication)

### Features
- Batch conversion of HEIC files
- Recursive directory processing
- Quality control for lossy formats
- Verbose/quiet output modes
- Cross-platform support (Linux, macOS, Windows)
- Type hints throughout codebase

### Technical
- Proper Python packaging with setuptools
- Comprehensive test coverage
- Code formatting with Black
- Import sorting with isort
- Linting with flake8
- Automated testing on multiple Python versions