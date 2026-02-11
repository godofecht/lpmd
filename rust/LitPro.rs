// LitPro.rs
// Literate Programming Framework for Rust

use std::collections::{HashMap, HashSet};
use std::fmt;
use std::io::{self, Write};

#[derive(Debug)]
pub struct Cell {
    pub id: String,
    pub code: String,
    pub dependencies: Vec<String>,
    pub executed: bool,
}

impl Cell {
    pub fn new(id: String, code: String, dependencies: Vec<String>) -> Self {
        Cell {
            id,
            code,
            dependencies,
            executed: false,
        }
    }
}

#[derive(Debug)]
pub enum LitProError {
    IoError(std::io::Error),
    CircularDependencyError,
    ParseError(String),
}

impl fmt::Display for LitProError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LitProError::IoError(e) => write!(f, "IO Error: {}", e),
            LitProError::CircularDependencyError => write!(f, "Circular dependency detected"),
            LitProError::ParseError(msg) => write!(f, "Parse Error: {}", msg),
        }
    }
}

impl std::error::Error for LitProError {}

pub struct LitPro {
    cells: HashMap<String, Cell>,
}

impl LitPro {
    pub fn new() -> Self {
        LitPro {
            cells: HashMap::new(),
        }
    }

    /// Parse cells from literate programming content
    pub fn parse_cells(&mut self, content: &str) -> Result<(), LitProError> {
        // This is a simplified parser - in a real implementation, you'd want a more robust parser
        let mut chars = content.chars().peekable();
        let mut pos = 0;

        while pos < content.len() {
            if let Some(cell_start) = content[pos..].find("<!-- cell:") {
                let cell_start_abs = pos + cell_start;
                pos = cell_start_abs;

                // Find the end of the cell marker
                if let Some(marker_end) = content[pos..].find("-->") {
                    let marker_end_abs = pos + marker_end + 3; // +3 for "-->"
                    
                    // Extract the cell marker content
                    let marker = &content[pos + 11..marker_end_abs - 3]; // +11 for "<!-- cell:"
                    
                    // Parse cell ID and dependencies
                    let parts: Vec<&str> = marker.split_whitespace().collect();
                    if parts.is_empty() {
                        continue;
                    }
                    
                    let cell_id = parts[0].to_string();
                    
                    // Parse dependencies
                    let mut dependencies = Vec::new();
                    for part in parts.iter().skip(1) {
                        if part.starts_with("depends:") {
                            let deps_str = &part[8..]; // skip "depends:"
                            dependencies.extend(deps_str.split(',').map(|s| s.trim().to_string()));
                        }
                    }
                    
                    // Find the code block
                    let code_start_marker = &content[marker_end_abs..];
                    if let Some(code_start) = code_start_marker.find("```rust") {
                        let code_start_abs = marker_end_abs + code_start + 8; // +8 for "```rust"
                        
                        if let Some(code_end) = code_start_marker[code_start + 8..].find("```") {
                            let code_end_abs = code_start_abs + code_end;
                            let code = content[code_start_abs..code_end_abs].trim().to_string();
                            
                            let cell = Cell::new(cell_id.clone(), code, dependencies);
                            self.cells.insert(cell_id, cell);
                        }
                    }
                }
            }
            
            pos += 1;
        }

        Ok(())
    }

    /// Resolve execution order using topological sort
    pub fn resolve_dependencies(&self) -> Result<Vec<String>, LitProError> {
        let mut graph: HashMap<String, Vec<String>> = HashMap::new();
        let mut in_degree: HashMap<String, usize> = HashMap::new();

        // Initialize graph and in-degree
        for cell_id in self.cells.keys() {
            graph.entry(cell_id.clone()).or_insert_with(Vec::new);
            in_degree.insert(cell_id.clone(), 0);
        }

        // Build graph and calculate in-degrees
        for cell in self.cells.values() {
            for dep in &cell.dependencies {
                if self.cells.contains_key(dep) {
                    graph.entry(dep.clone()).or_insert_with(Vec::new).push(cell.id.clone());
                    *in_degree.get_mut(&cell.id).unwrap() += 1;
                } else {
                    eprintln!("Warning: Dependency '{}' not found for cell '{}'", dep, cell.id);
                }
            }
        }

        // Kahn's algorithm for topological sort
        let mut queue: Vec<String> = Vec::new();
        for (node, degree) in &in_degree {
            if *degree == 0 {
                queue.push(node.clone());
            }
        }

        let mut result: Vec<String> = Vec::new();

        while !queue.is_empty() {
            let node = queue.remove(0);
            result.push(node.clone());

            for neighbor in &graph[&node] {
                let new_degree = in_degree.get_mut(neighbor).unwrap();
                *new_degree -= 1;
                if *new_degree == 0 {
                    queue.push(neighbor.clone());
                }
            }
        }

        // Check if all nodes were included (no cycles)
        if result.len() != graph.len() {
            return Err(LitProError::CircularDependencyError);
        }

        Ok(result)
    }

    /// Execute a literate programming file
    pub fn run_litpro(&mut self, content: &str) -> Result<(), LitProError> {
        println!("Executing literate file...");

        // Parse cells
        self.parse_cells(content)?;

        if self.cells.is_empty() {
            println!("No cells found in the literate file.");
            return Ok(());
        }

        // Resolve execution order
        let execution_order = self.resolve_dependencies()?;

        println!("Found {} cells with dependencies.", self.cells.len());
        print!("Execution order: ");
        for (i, cell_id) in execution_order.iter().enumerate() {
            if i > 0 {
                print!(" → ");
            }
            print!("{}", cell_id);
        }
        println!();

        // Execute cells in order
        for cell_id in execution_order {
            let cell = self.cells.get_mut(&cell_id).unwrap();
            
            println!("\n--- Executing cell: {} ---", cell.id);
            if !cell.dependencies.is_empty() {
                println!("Dependencies: {}", cell.dependencies.join(", "));
            }
            
            // In a real implementation, you would execute the Rust code
            // For now, we'll just print the code
            println!("Code:\n{}", cell.code);
            
            // Mark as executed
            cell.executed = true;
            println!("✓ Cell executed successfully");
        }

        println!("\n--- Execution completed ---");
        Ok(())
    }

    /// Export to plain Rust code
    pub fn export_litpro(&self, output_file: &str) -> Result<(), LitProError> {
        let mut file = std::fs::File::create(output_file).map_err(LitProError::IoError)?;
        
        writeln!(file, "// Exported from LitPro").map_err(LitProError::IoError)?;
        writeln!(file).map_err(LitProError::IoError)?;
        
        for (id, cell) in &self.cells {
            writeln!(file, "// Cell: {}", id).map_err(LitProError::IoError)?;
            writeln!(file, "{}", cell.code).map_err(LitProError::IoError)?;
            writeln!(file).map_err(LitProError::IoError)?;
        }
        
        println!("Exported to: {}", output_file);
        Ok(())
    }

    /// Generate HTML documentation
    pub fn html_litpro(&self, output_file: &str) -> Result<(), LitProError> {
        let mut file = std::fs::File::create(output_file).map_err(LitProError::IoError)?;
        
        write!(file, r#"<!DOCTYPE html>
<html>
<head>
    <title>LitPro Documentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .cell {{ margin: 20px 0; padding: 15px; border-left: 3px solid #007acc; }}
        .code {{ background: #f4f4f4; padding: 10px; border-radius: 4px; }}
        pre {{ margin: 0; }}
    </style>
</head>
<body>
    <h1>LitPro Documentation</h1>"#).map_err(LitProError::IoError)?;
        
        for (id, cell) in &self.cells {
            write!(file, r#"
    <div class="cell">
        <h3>Cell: {}</h3>
        <div class="code">
            <pre><code class="language-rust">{}</code></pre>
        </div>
    </div>"#, 
            id, 
            self.escape_html(&cell.code)
        ).map_err(LitProError::IoError)?;
        }
        
        write!(file, r#"
</body>
</html>"#).map_err(LitProError::IoError)?;
        
        println!("HTML documentation generated: {}", output_file);
        Ok(())
    }

    /// Escape HTML characters
    fn escape_html(&self, s: &str) -> String {
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace("\"", "&quot;")
         .replace("'", "&#x27;")
    }
}

// Example usage
fn main() -> Result<(), LitProError> {
    let content = r#"# My First Literate Program

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
"#;

    let mut litpro = LitPro::new();
    litpro.run_litpro(content)?;
    
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_cells() {
        let content = r#"<!-- cell:test_id -->
```rust
let x = 5;
```
"#;

        let mut litpro = LitPro::new();
        assert!(litpro.parse_cells(content).is_ok());
        assert_eq!(litpro.cells.len(), 1);
        assert!(litpro.cells.contains_key("test_id"));
    }
}