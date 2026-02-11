<div align="center">
  <h1>Literate Python Markdown (LPMD)</h1>
  <p><strong>Revolutionary executable literate programming for the modern era</strong></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
  [![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/abhishekshivakumar/lpmd_project)
  
</div>

<br />

## Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## About

Literate Python Markdown (LPMD) is a revolutionary technology that allows you to write and execute interactive Python programs directly in markdown files. Unlike traditional literate programming that only displays code, LPMD **actually runs** your markdown documents as executable programs.

This project combines the readability of markdown with the power of executable code, enabling a new paradigm for technical documentation, educational content, and reproducible research.

### Why LPMD?
- **Readable**: Clean markdown syntax that renders beautifully everywhere
- **Executable**: Actually runs your code as part of the documentation
- **Modular**: Cell-based execution with dependency management
- **Flexible**: Works with any Python library or framework

## Features

- Cell-Based Execution: Code organized in executable cells with dependency management
- Smart Dependencies: Cells run in dependency order using topological sort
- Variable Persistence: Share variables between cells with explicit persistence
- Interactive Execution: Execute cells individually or run complete programs
- Markdown Native: Pure markdown format, readable in any editor
- Python Powered: Full Python execution with state management
- Web Integration: Generate HTML output and run in browsers
- Audio Processing: Built-in support for audio processing examples

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Quick Install
```bash
# Clone the repository
git clone https://github.com/abhishekshivakumar/lpmd_project.git
cd lpmd_project

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Optional Dependencies (for audio processing)
```bash
pip install torch torchvision torchaudio
```

## Usage

### Creating Your First LPMD File

Create a file named `hello.lpmd`:

```markdown
# My First Literate Program

<!-- cell:setup -->
```python
print("Hello from LPMD!")
x = 10
y = 20
```

<!-- cell:compute depends:setup -->
```python
result = x + y
print(f"Sum: {result}")
```

<!-- cell:display depends:compute -->
```python
print(f"The final result is: {result}")
```
```

### Running LPMD Files

Execute your LPMD file:

```bash
python src/core/lpmd_executor.py hello.lpmd
# Or auto-confirm:
python src/core/lpmd_executor.py hello.lpmd --yes
```

### Cell Syntax

```markdown
<!-- cell:cell_id [depends:dep1,dep2] [persist:var1,var2] -->
```python
# Your Python code here
code goes here
```
```

Parameters:
- `cell_id`: Unique identifier for the cell
- `depends`: Comma-separated list of cells this cell depends on
- `persist`: Variables to explicitly persist (optional, all variables persist by default)

## Examples

### Basic Arithmetic
```markdown
<!-- cell:initialize -->
```python
a = 5
b = 10
print(f"a = {a}, b = {b}")
```

<!-- cell:calculate depends:initialize -->
```python
result = a * b
print(f"Result: {result}")
```
```

### Audio Processing
Check out `examples/interactive_audio_demo.md` for a complete audio processing example with the 4096-band multi-band compressor.

### Data Analysis
See `examples/data_analysis.lpmd` for data science workflows.

## API Reference

### Core Components

#### lpmd_executor.py
Main execution engine for LPMD files.

- `execute_lpmd(file_path, auto_confirm=False)`: Execute an LPMD file
- `parse_cells(content)`: Parse cells from LPMD content
- `resolve_dependencies(cells)`: Resolve execution order based on dependencies

#### lpmd_html_generator.py
Convert LPMD files to HTML.

- `generate_html(lpmd_content)`: Generate HTML from LPMD content
- `save_html(html_content, output_path)`: Save HTML to file

#### lpmd_web_server.py
Web interface for interactive LPMD development.

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/lpmd_project.git
cd lpmd_project

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Inspired by Donald Knuth's concept of literate programming
- Built with Python's powerful execution capabilities
- Designed for modern development workflows
- Special thanks to the open-source community for inspiration and tools

## Contact

- **Maintainer**: Abhishek Shivakumar
- **Email**: [abhishek@example.com](mailto:abhishek@example.com)
- **Repository**: [https://github.com/abhishekshivakumar/lpmd_project](https://github.com/abhishekshivakumar/lpmd_project)

---

<div align="center">
  <sub>Built with love by <a href="https://github.com/abhishekshivakumar">Abhishek Shivakumar</a></sub>
</div>

<div align="center">
  <sub>Literate Python Markdown - Revolutionizing how we write and execute computational narratives</sub>
</div>