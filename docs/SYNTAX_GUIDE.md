# Literate Python Markdown (LPMD) Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Syntax Guide](#syntax-guide)
5. [Advanced Features](#advanced-features)
6. [Examples](#examples)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

## Introduction

Literate Python Markdown (LPMD) is a revolutionary technology that allows you to write and execute interactive Python programs directly in markdown files. Unlike traditional literate programming that only displays code, LPMD **actually runs** your markdown documents as executable programs.

### Key Concepts

- **Cells**: Code blocks with execution metadata
- **Dependencies**: Execution order based on cell relationships
- **Persistence**: Variable sharing between cells
- **Invisible Syntax**: HTML comments for clean markdown appearance

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Optional Dependencies
For audio processing examples:
```bash
pip install torch torchvision torchaudio
```

## Quick Start

### Creating Your First LPMD File

Create a file named `hello.lpmd`:

```markdown
# My First LPMD Document

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
```

## Syntax Guide

### Cell Definition

```markdown
<!-- cell:cell_id [depends:dep1,dep2] [persist:var1,var2] -->
```python
# Your Python code here
code goes here
```
```

### Parameters
- `cell_id`: Unique identifier for the cell
- `depends`: Comma-separated list of cells this cell depends on
- `persist`: Variables to explicitly persist (optional)

### Cell Types

#### Basic Cell
```markdown
<!-- cell:my_cell -->
```python
x = 42
print(x)
```
```

#### Dependent Cell
```markdown
<!-- cell:dependent_cell depends:my_cell -->
```python
# Can access variable x from my_cell
y = x * 2
print(y)
```
```

#### Persistent Cell
```markdown
<!-- cell:persistent_cell persist:data,model -->
```python
data = load_data()
model = create_model()
```
```

## Advanced Features

### Variable Persistence

By default, all variables are shared between dependent cells:

```markdown
<!-- cell:math -->
```python
import math
PI = math.pi
radius = 5
```

<!-- cell:area depends:math -->
```python
# Can use PI and radius from previous cell
area = PI * radius ** 2
print(f"Area: {area}")
```
```

### Execution Order

Cells are automatically sorted using topological sort based on dependencies:

```
A → B → C    # A runs first, then B, then C
    ↘ D      # D runs after B
```

### Error Handling

If a cell fails, execution stops with detailed error information:

```
❌ Error in cell compute: ZeroDivisionError: division by zero
  File "<string>", line 3, in <module>
    result = 1 / 0
ZeroDivisionError: division by zero
```

## Examples

### Basic Arithmetic
See `examples/basic_arithmetic.lpmd`

### Data Analysis
See `examples/data_analysis.lpmd`

### Audio Processing
See `examples/interactive_audio_demo.md`

### Machine Learning
See `examples/ml_pipeline.lpmd`

## API Reference

### lpmd_executor.py

Main execution engine for LPMD files.

#### Functions

- `execute_lpmd(file_path, auto_confirm=False)`: Execute an LPMD file
- `parse_cells(content)`: Parse cells from LPMD content
- `resolve_dependencies(cells)`: Resolve execution order based on dependencies

### lpmd_html_generator.py

Convert LPMD files to HTML.

#### Functions

- `generate_html(lpmd_content)`: Generate HTML from LPMD content
- `save_html(html_content, output_path)`: Save HTML to file

## Troubleshooting

### Common Issues

#### Cell Dependencies Not Working
Make sure cell IDs are unique and dependency references are correct.

#### Variables Not Persisting
Check that dependent cells are properly declared with the `depends` parameter.

#### Syntax Errors
Ensure cell markers use the correct HTML comment syntax.

### Getting Help

- Check the examples in the `examples/` directory
- Review the syntax guide above
- Look at the API reference for implementation details

## Contributing

See the contributing guidelines in the main README.