# LitPro.rs - Literate Programming Framework for Rust

LitPro.rs brings the power of literate programming to the Rust ecosystem. Write executable documents that combine narrative text with Rust code, with explicit dependency management between code blocks.

## Features

- **Cell-Based Execution**: Code organized in executable cells with dependency management
- **Smart Dependencies**: Cells run in dependency order using topological sort
- **Markdown Native**: Uses markdown format with special cell markers
- **Rust Powered**: Full access to Rust's performance and safety features
- **Easy Export**: Export to plain Rust code or HTML documentation

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
litpro = "1.0.0"
```

Or clone the repository:

```bash
git clone https://github.com/godofecht/litpro_rust.git
```

## Usage

Create a literate programming file (e.g., `example.lit`):

```markdown
# My First Literate Program

<!-- cell:setup -->
```rust
println!("Hello from LitPro.rs!");
let x = 10;
let y = 20;
```

<!-- cell:compute depends:setup -->
```rust
let result = x + y;
println!("Sum: {}", result);
```

<!-- cell:display depends:compute -->
```rust
println!("The final result is: {}", result);
```
```

Then execute it in Rust:

```rust
use litpro::LitPro;

fn main() -> Result<(), LitProError> {
    let content = std::fs::read_to_string("example.lit")?;
    
    let mut litpro = LitPro::new();
    litpro.run_litpro(&content)?;
    
    Ok(())
}
```

## Cell Syntax

LitPro.rs uses HTML comments as cell markers to keep the markdown readable while enabling execution:

```markdown
<!-- cell:cell_id [depends:dep1,dep2] -->
```rust
// Your Rust code here
code goes here
```
```

Parameters:
- `cell_id`: Unique identifier for the cell
- `depends`: Comma-separated list of cells this cell depends on

## API Reference

### Structs
- `LitPro`: Main struct for the framework
- `Cell`: Represents a single code cell
- `LitProError`: Error types for the framework

### Methods
- `LitPro::new()`: Create a new LitPro instance
- `litpro.parse_cells(content)`: Parse cells from content
- `litpro.run_litpro(content)`: Execute literate programming content
- `litpro.export_litpro(output_file)`: Export to plain Rust code
- `litpro.html_litpro(output_file)`: Generate HTML documentation
- `litpro.resolve_dependencies()`: Resolve execution order

## Examples

### Basic Arithmetic

```markdown
<!-- cell:initialize -->
```rust
let a = 5;
let b = 10;
println!("a = {}, b = {}", a, b);
```

<!-- cell:calculate depends:initialize -->
```rust
let result = a * b;
println!("Result: {}", result);
```
```

### Rust-Specific Example

```markdown
<!-- cell:setup -->
```rust
use std::collections::HashMap;
use std::time::Instant;

println!("Rust setup complete");
let start_time = Instant::now();
```

<!-- cell:data-processing depends:setup -->
```rust
let mut data: HashMap<String, i32> = HashMap::new();
data.insert("item1".to_string(), 100);
data.insert("item2".to_string(), 200);

let total: i32 = data.values().sum();
println!("Total: {}", total);

let elapsed = start_time.elapsed();
println!("Processing took: {:?}", elapsed);
```
```

## How It Works

1. LitPro.rs parses the file to identify cells and their dependencies
2. It resolves execution order using topological sorting
3. Cells are executed in dependency order
4. Output is displayed as the code executes

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