# Publishing LPMD to PyPI

This guide explains how to publish the Literate Python Markdown (LPMD) package to the Python Package Index (PyPI).

## Prerequisites

1. **PyPI Account**: Create an account on [PyPI](https://pypi.org/account/register/)
2. **API Token**: Generate an API token in your PyPI account settings
3. **GitHub Secrets**: Add your PyPI API token to your GitHub repository secrets

## Steps to Publish

### 1. Add PyPI API Token to GitHub Secrets

1. Go to your GitHub repository: https://github.com/godofecht/lpmd
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name it `PYPI_API_TOKEN`
5. Paste your PyPI API token as the value
6. Click "Add secret"

### 2. Create a Release

To trigger the automatic PyPI publication:

1. Go to your GitHub repository releases: https://github.com/godofecht/lpmd/releases
2. Click "Draft a new release"
3. Create a tag (e.g., `v1.0.0`) - this should match the version in setup.py
4. Add a title (e.g., "Version 1.0.0")
5. Describe the changes in the release notes
6. Click "Publish release"

### 3. Automatic Publication

Once you publish the release, GitHub Actions will automatically:
1. Checkout the tagged code
2. Set up Python environment
3. Install build dependencies
4. Build the package (source distribution and wheel)
5. Upload to PyPI using your API token

## Manual Publication (Alternative Method)

If you prefer to publish manually:

1. Install build tools:
   ```bash
   pip install build twine
   ```

2. Build the package:
   ```bash
   python -m build
   ```

3. Upload to PyPI:
   ```bash
   twine upload dist/* --username __token__ --password YOUR_PYPI_API_TOKEN
   ```

## Verification

After publication, verify the package is available at:
https://pypi.org/project/lpmd/

## Installation

Once published, users can install your package with:
```bash
pip install lpmd
```

## Usage

After installation, users can:
- Execute LPMD files: `lpmd-execute myfile.lpmd`
- Generate HTML: `lpmd-generate-html myfile.lpmd`
- Import in Python: `from lpmd.core import lpmd_executor`

## Notes

- The package version is controlled in `setup.py` and the `__version__` attribute in `src/core/lpmd_executor.py`
- The GitHub Actions workflow only runs on release publication, not on pushes to main
- Make sure to update the version number before creating a new release