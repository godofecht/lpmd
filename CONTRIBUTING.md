# Contributing to Literate Python Markdown (LPMD)

Thank you for your interest in contributing to LPMD! This document outlines the process for contributing to the project.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Code Style](#code-style)
4. [Testing](#testing)
5. [Submitting Changes](#submitting-changes)
6. [Project Structure](#project-structure)

## Getting Started

Before contributing, please ensure you have:

- A GitHub account
- Git installed on your system
- Python 3.7+ installed
- Familiarity with the LPMD syntax and concepts

## Development Setup

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/lpmd_project.git
   cd lpmd_project
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Code Style

### Python Code
- Follow PEP 8 style guidelines
- Use 4 spaces for indentation
- Maximum line length of 100 characters
- Use descriptive variable and function names
- Include docstrings for all public functions and classes

### LPMD Files
- Use consistent cell naming conventions
- Include meaningful comments in code blocks
- Maintain clear dependency chains
- Use the invisible HTML comment syntax

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters or less
- Reference issues and pull requests liberally

## Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_basic.py

# Run with verbose output
python -m pytest -v
```

### Adding Tests
When adding new features or fixing bugs, please include appropriate tests:

1. Create test files in the `tests/` directory
2. Follow the naming convention `test_*.py`
3. Use descriptive test function names
4. Test both positive and negative cases

## Submitting Changes

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/my-awesome-feature
   ```
   
2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "Add my awesome feature"
   ```

3. Push your changes to your fork:
   ```bash
   git push origin feature/my-awesome-feature
   ```

4. Open a pull request on GitHub

### Pull Request Guidelines

- Fill out the pull request template completely
- Describe the problem and solution clearly
- Include screenshots if UI changes are involved
- Link to any relevant issues
- Ensure all tests pass before submitting

## Project Structure

```
lpmd_project/
├── src/                    # Source code
│   ├── core/              # Core LPMD functionality
│   ├── utils/             # Utility scripts
│   └── web/               # Web interface components
├── examples/              # Example LPMD files
├── docs/                  # Documentation
├── tests/                 # Test files
├── dist/                  # Distribution files
└── ...
```

## Development Workflow

### Feature Development
1. Create an issue describing the feature
2. Discuss the approach with maintainers
3. Create a branch for the feature
4. Implement the feature with tests
5. Submit a pull request

### Bug Fixes
1. Create an issue describing the bug (if it doesn't exist)
2. Create a branch for the fix
3. Add a test that reproduces the bug
4. Implement the fix
5. Submit a pull request

## Questions?

If you have questions about contributing, feel free to open an issue with the "question" label.

Thank you for contributing to LPMD!