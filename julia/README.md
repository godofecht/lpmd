# LitPro.jl - Literate Programming Framework for Julia

LitPro.jl brings the power of literate programming to the Julia ecosystem. Write executable documents that combine narrative text with Julia code, with explicit dependency management between code blocks.

## Features

- **Cell-Based Execution**: Code organized in executable cells with dependency management
- **Smart Dependencies**: Cells run in dependency order using topological sort
- **Markdown Native**: Uses markdown format with special cell markers
- **Julia Powered**: Full access to Julia's high-performance computing capabilities
- **Easy Export**: Export to plain Julia code or HTML documentation

## Installation

```julia
# In Julia REPL:
using Pkg
Pkg.add(url="https://github.com/godofecht/litpro_julia.git")
```

Or manually download the `LitPro.jl` file and include it in your project.

## Usage

### Basic Usage

Create a literate programming file (e.g., `example.lit`):

```markdown
# My First Literate Program

<!-- cell:setup -->
```julia
println("Hello from LitPro.jl!")
x = 10
y = 20
```

<!-- cell:compute depends:setup -->
```julia
result = x + y
println("Sum: \$result")
```

<!-- cell:display depends:compute -->
```julia
println("The final result is: \$result")
```
```

Then execute it in Julia:

```julia
include("LitPro.jl")
using .LitPro

# Execute the literate file
run_litpro("example.lit")
```

### Using the Macro

```julia
# Execute directly with macro
@litpro "example.lit"
```

### Export to Plain Code

```julia
# Export to plain Julia code
export_litpro("example.lit", "example.jl")
```

### Generate HTML Documentation

```julia
# Generate HTML documentation
html_litpro("example.lit", "example.html")
```

## Cell Syntax

LitPro.jl uses HTML comments as cell markers to keep the markdown readable while enabling execution:

```markdown
<!-- cell:cell_id [depends:dep1,dep2] -->
```julia
# Your Julia code here
code goes here
```
```

Parameters:
- `cell_id`: Unique identifier for the cell
- `depends`: Comma-separated list of cells this cell depends on

## API Reference

### Functions

- `run_litpro(filename)`: Execute a literate programming file
- `export_litpro(filename, output_file)`: Export to plain Julia code
- `html_litpro(filename, output_file)`: Generate HTML documentation
- `@litpro filename`: Macro to execute a literate file

## Examples

### Basic Arithmetic

```markdown
<!-- cell:initialize -->
```julia
a = 5
b = 10
println("a = \$a, b = \$b")
```

<!-- cell:calculate depends:initialize -->
```julia
result = a * b
println("Result: \$result")
```
```

### Scientific Computing Example

```markdown
<!-- cell:setup -->
```julia
using LinearAlgebra
using Random

Random.seed!(42)
println("Julia scientific computing setup complete")
```

<!-- cell:matrix-op depends:setup -->
```julia
A = rand(5, 5)
B = rand(5, 5)
C = A * B
println("Matrix multiplication completed")
println("Size of result: \$(size(C))")
```
```

## How It Works

1. LitPro.jl parses the file to identify cells and their dependencies
2. It resolves execution order using topological sorting
3. Cells are executed in dependency order
4. Variables are shared between dependent cells
5. Output is displayed as the code executes

## Advantages Over Notebooks

- **Explicit Dependencies**: Every dependency is declared, preventing hidden state issues
- **Deterministic Execution**: Same inputs always produce same outputs, regardless of execution history
- **Flexible Narrative**: Narrative order is independent of execution order
- **Version Control Friendly**: Clean text-based format without binary outputs
- **True Literate Programming**: Document is primary, code is derived

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.