<div align="center">
  <h1>LitPro - Literate Programming Framework</h1>
  <p><strong>Modern executable literate programming for any language</strong></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
  [![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/godofecht/litpro)
  
</div>

<br />

## Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Embedding in Websites](#embedding-in-websites)
- [Language Adapters](#language-adapters)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## About

LitPro is a modern literate programming framework that allows you to write and execute interactive programs directly in markdown files. Unlike traditional literate programming that only displays code, LitPro **actually runs** your documents as executable programs.

This project combines the readability of markdown with the power of executable code, enabling a new paradigm for technical documentation, educational content, and reproducible research. The framework is designed to be language-agnostic, supporting Python, JavaScript, Rust, and more.

### Why LitPro?
- **Readable**: Clean markdown syntax that renders beautifully everywhere
- **Executable**: Actually runs your code as part of the documentation
- **Modular**: Cell-based execution with dependency management
- **Flexible**: Works with any programming language ecosystem
- **Deterministic**: No hidden state, reproducible results every time
- **Language-Agnostic**: Easy to extend to other programming languages

## Features

- **Cell-Based Execution**: Code organized in executable cells with dependency management
- **Smart Dependencies**: Cells run in dependency order using topological sort
- **Variable Persistence**: Share variables between cells with explicit persistence
- **Interactive Execution**: Execute cells individually or run complete programs
- **Markdown Native**: Pure markdown format, readable in any editor
- **Multi-Language Support**: Framework designed for any programming language
- **Web Integration**: Generate HTML output and run in browsers
- **Website Embedding**: Easy integration into blogs and documentation sites

## Installation

### Quick Install
```bash
pip install litpro
```

### From Source
```bash
# Clone the repository
git clone https://github.com/godofecht/litpro.git
cd litpro

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

### Simple Commands

```bash
# Execute a literate file
litpro run myfile.lit

# Export to plain code
litpro export myfile.lit

# Generate HTML documentation
litpro html myfile.lit
```

### Creating Your First LitPro File

Create a file named `hello.lit`:

```markdown
# My First Literate Program

<!-- cell:setup -->
```python
print("Hello from LitPro!")
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
See `examples/data_analysis.lit` for data science workflows.

## API Reference

### Core Components

#### litpro_executor.py
Main execution engine for LitPro files.

- `execute_litpro(file_path, auto_confirm=False)`: Execute a LitPro file
- `parse_cells(content)`: Parse cells from LitPro content
- `resolve_dependencies(cells)`: Resolve execution order based on dependencies

#### litpro_html_generator.py
Convert LitPro files to HTML.

- `generate_html(litpro_content)`: Generate HTML from LitPro content
- `save_html(html_content, output_path)`: Save HTML to file

#### litpro_web_server.py
Web interface for interactive LitPro development.

## Embedding in Websites

LitPro can be embedded directly in websites and blogs:

### Web Component
```html
<script src="https://cdn.jsdelivr.net/npm/litpro-web-component@latest/litpro-runner.js"></script>
<litpro-runner>
  <pre><code>
    <!-- cell:setup -->
    ```python
    print("Hello from LitPro!")
    x = 10
    ```
  </code></pre>
</litpro-runner>
```

### JavaScript API
```html
<script>
  import { LitPro } from 'litpro-web-component';

  const litpro = new LitPro({
    selector: '#litpro-container',
    code: `<!-- cell:setup -->
      ```python
      print("Hello from LitPro!")
      x = 10
      ```
      <!-- cell:compute depends:setup -->
      ```python
      result = x * 2
      print(f"Result: {result}")
      ```
    `
  });

  litpro.render();
</script>
```

## Language Implementations

LitPro provides complete implementations for multiple programming languages:

### Python (Primary Implementation)
- **Location**: `src/`
- **Commands**: `litpro run`, `litpro export`, `litpro html`
- **File Extension**: `.lit`, `.lpmd`, `.md`
- **Features**: Full implementation with web interface

### Julia Implementation
LitPro is available for the Julia programming language! The Julia implementation provides the same literate programming capabilities with Julia-specific optimizations.

**Features:**
- Full Julia language support
- High-performance numerical computing
- Integration with Julia's package ecosystem
- Cell-based execution with dependency management

**Installation:**
```julia
# In Julia REPL:
include("julia/LitPro.jl")
using .LitPro
```

**Usage:**
```julia
# Execute a literate file
run_litpro("example.lit")

# Export to plain Julia code
export_litpro("example.lit", "output.jl")

# Generate HTML documentation
html_litpro("example.lit", "output.html")
```

**Example:**
```markdown
<!-- cell:setup -->
```julia
using LinearAlgebra
println("Julia setup complete")
x = 10
```

<!-- cell:compute depends:setup -->
```julia
result = x * 2
println("Result: \$result")
```
```

### JavaScript Implementation
LitPro is available for JavaScript with both Node.js and browser support.

**Features:**
- Node.js and browser compatibility
- Full dependency resolution
- Export and HTML generation capabilities

**Installation:**
```bash
npm install litpro-js
```

**Usage:**
```javascript
const LitPro = require('litpro-js');
const fs = require('fs');

const content = fs.readFileSync('example.lit', 'utf8');
const litpro = new LitPro();

await litpro.runLitPro(content);
```

### Rust Implementation
LitPro is available for Rust with memory safety and performance benefits.

**Features:**
- Memory-safe execution
- High-performance compilation
- Dependency resolution with error handling

**Usage:**
```rust
use litpro::LitPro;

fn main() -> Result<(), LitProError> {
    let content = std::fs::read_to_string("example.lit")?;
    
    let mut litpro = LitPro::new();
    litpro.run_litpro(&content)?;
    
    Ok(())
}
```

### Adding New Languages

LitPro's architecture makes it easy to extend to other programming languages:

#### Creating a Language Implementation

Each language implementation should provide:
- Code parser for the language
- Dependency resolver
- Execution environment
- Error formatter
- Export functionality
- HTML generation

#### Example: JavaScript Implementation Structure
```javascript
// LitPro.js
class LitPro {
  parseCells(content) { /* parse cells */ }
  resolveDependencies(cells) { /* resolve deps */ }
  runLitPro(content) { /* execute */ }
  exportLitPro(content, output) { /* export */ }
  htmlLitPro(content, output) { /* generate html */ }
}
```

### Planned Language Support
- Go
- R
- C/C++

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
git clone https://github.com/YOUR_USERNAME/litpro.git
cd litpro

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
- **Repository**: [https://github.com/godofecht/litpro](https://github.com/godofecht/litpro)

---

<div align="center">
  <sub>Built with love by <a href="https://github.com/godofecht">Abhishek Shivakumar</a></sub>
</div>

<div align="center">
  <sub>LitPro - Revolutionizing how we write and execute computational narratives</sub>
</div>