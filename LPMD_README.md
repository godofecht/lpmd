# Literate Python Markdown (.lpmd) - A New Technology

> **Revolutionary markdown-based execution for literate programming**

## What is Literate Python Markdown?

Literate Python Markdown (`.lpmd`) is a **new execution technology** that allows you to write and execute interactive Python programs directly in markdown files. Unlike traditional literate programming that only displays code, LPMD **actually runs** your markdown documents as executable programs.

## 🚀 Key Innovation: Cell-Based Execution with Dependencies

Traditional markdown code blocks are static. LPMD introduces **executable cells** with dependency management:

```markdown
--- cell:init ---
```python
# This runs first
import torch
x = 42
```

--- cell:compute depends:init ---
```python
# This runs after init (can use x)
result = x * 2
print(f"Result: {result}")
```

--- cell:display depends:compute persist:result ---
```python
# This runs last (result persists)
print(f"Final result: {result}")
```
```

## 🎯 Features

- **📦 Cell-Based Execution**: Code organized in executable cells
- **🔗 Dependency Management**: Cells run in dependency order using topological sort
- **💾 Variable Persistence**: Share variables between cells with explicit persistence
- **🎮 Interactive**: Execute cells individually or run complete programs
- **📝 Markdown Native**: Pure markdown format, readable in any editor
- **🐍 Python Powered**: Full Python execution with state management

## Installation

```bash
# The executor is in your current directory
# Make sure PyTorch is installed for the demo
pip install torch numpy
```

## Quick Start

1. **Create a .lpmd file:**

```markdown
# My First Literate Program

--- cell:setup ---
```python
print("Hello from LPMD!")
x = 10
```

--- cell:compute depends:setup ---
```python
result = x * 42
print(f"Answer: {result}")
```
```

2. **Execute it:**

```bash
python lpmd_executor.py my_program.lpmd
# Or auto-confirm:
python lpmd_executor.py my_program.lpmd --yes
```

## Syntax Reference

### Cell Definition
```markdown
<!-- cell:cell_id [depends:dep1,dep2] [persist:var1,var2] -->
```python
# Your Python code here
code goes here
```
```

### Invisible Syntax (Recommended)

LPMD uses HTML comments (`<!-- -->`) for cell markers, making them **completely invisible** in markdown previews and editors! This gives you the cleanest possible reading experience while maintaining full execution capabilities.

**What viewers see:**
```markdown
# Your Document Title

This is your content with normal markdown formatting.

```python
# Your code appears normally with syntax highlighting
print("Hello from an executable cell!")
```

More content here...
```

**What the executor sees:**
```markdown
<!-- cell:example_cell depends:previous_cell -->
```python
# Your code appears normally with syntax highlighting
print("Hello from an executable cell!")
```
<!-- cell:next_cell depends:example_cell -->
```

### Backward Compatibility

LPMD also supports the visible syntax for compatibility:
```markdown
--- cell:cell_id [depends:dep1,dep2] ---
```python
code here
```
---
```

### Parameters
- `cell_id`: Unique identifier for the cell
- `depends`: Comma-separated list of cells this cell depends on
- `persist`: Variables to explicitly persist (optional, all variables persist by default)

### Execution Order
Cells are automatically sorted using topological sort based on dependencies:

```
A → B → C    # A runs first, then B, then C
    ↘ D      # D runs after B
```

## Advanced Features

### Variable Persistence

By default, all variables are shared between dependent cells:

```markdown
--- cell:math ---
```python
import math
PI = math.pi
radius = 5
```

--- cell:area depends:math ---
```python
# Can use PI and radius from previous cell
area = PI * radius ** 2
print(f"Area: {area}")
```
```

### Explicit Persistence

Use `persist:` to mark variables that should definitely carry over:

```markdown
--- cell:load_data persist:data,model ---
```python
data = load_dataset()
model = create_model()
```

--- cell:train depends:load_data ---
```python
# data and model are guaranteed to be available
train_model(model, data)
```
```

### Error Handling

If a cell fails, execution stops with detailed error information:

```
❌ Error in cell compute: ZeroDivisionError: division by zero
  File "<string>", line 3, in <module>
    result = 1 / 0
ZeroDivisionError: division by zero
```

## Real-World Example

See `literate_python.md` for a complete example that demonstrates:

- Multi-band audio compression
- Frequency domain processing
- State persistence across cells
- Dependency management
- Data visualization preparation

## Comparison with Other Technologies

| Technology | Execution | Dependencies | State Management | Format |
|------------|-----------|--------------|------------------|--------|
| **LPMD** | ✅ Native | ✅ Topological | ✅ Full Python | Markdown |
| Jupyter | ✅ Native | ❌ Manual | ✅ Full Python | JSON |
| R Markdown | ✅ External | ❌ Limited | ✅ Language | Markdown |
| Traditional LP | ❌ Display only | ❌ None | ❌ None | Various |

## Use Cases

- **📚 Educational Content**: Executable tutorials and lessons
- **🔬 Research Notebooks**: Reproducible analysis workflows
- **📊 Data Science**: Interactive exploration with narrative
- **🎵 Audio Processing**: Real-time algorithm prototyping
- **🤖 ML Experiments**: Version-controlled, executable experiments

## Technical Implementation

The LPMD executor uses:

- **Topological Sort**: Resolves execution order from dependencies
- **Python exec()**: Executes code in managed namespaces
- **State Management**: Global namespace shared between cells
- **Output Capture**: stdout redirection for clean display
- **Error Propagation**: Comprehensive error reporting

## Future Enhancements

- **Interactive Mode**: Execute individual cells on demand
- **Caching**: Skip unchanged cells for faster iteration
- **Export**: Convert to Jupyter notebooks or other formats
- **Parallel Execution**: Run independent cells concurrently
- **Rich Output**: Support for images, HTML, and interactive widgets

---

**Literate Python Markdown revolutionizes how we write and execute computational narratives. Code and documentation are no longer separate - they're one executable story.** 🎉
