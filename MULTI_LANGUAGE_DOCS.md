# LitPro - Multi-Language Literate Programming Framework

LitPro is a framework for literate programming that works across multiple programming languages. This document provides an overview of all language implementations and how to use them.

## Supported Languages

### Python (Primary Implementation)
- **Location**: Root directory and `src/`
- **Commands**: `litpro run`, `litpro export`, `litpro html`
- **File Extension**: `.lit`, `.lpmd`, `.md`
- **Features**: Full implementation with web interface

### Julia
- **Location**: `julia/`
- **Commands**: `run_litpro()`, `export_litpro()`, `html_litpro()`
- **File Extension**: `.lit`
- **Features**: High-performance numerical computing

### JavaScript
- **Location**: `js/`
- **Commands**: `LitPro` class methods
- **File Extension**: `.lit`
- **Features**: Browser and Node.js support

### Rust
- **Location**: `rust/`
- **Commands**: `LitPro` struct methods
- **File Extension**: `.lit`
- **Features**: Memory safety and performance

## Common Syntax

All implementations use the same cell syntax:

```markdown
<!-- cell:cell_id [depends:dep1,dep2] -->
```language
// Your code here
```
```

## Directory Structure

```
litpro/
├── src/                 # Python implementation
│   ├── core/           # Core functionality
│   ├── utils/          # Utilities
│   └── web/            # Web interface
├── julia/              # Julia implementation
│   ├── LitPro.jl       # Main module
│   ├── Project.toml    # Package info
│   ├── README.md       # Documentation
│   └── example.lit     # Example file
├── js/                 # JavaScript implementation
│   ├── LitPro.js       # Main module
│   └── README.md       # Documentation
├── rust/               # Rust implementation
│   ├── LitPro.rs       # Main module
│   └── README.md       # Documentation
├── go/                 # Go implementation (coming soon)
├── r/                  # R implementation (coming soon)
├── .github/workflows/  # CI/CD workflows
├── README.md           # Main documentation
├── LLM_GUIDE.md        # Guide for LLMs
└── ...
```

## Building Packages

The GitHub Actions workflows in `.github/workflows/` automatically build packages for each language when changes are pushed to the main branch.

## Adding New Languages

To add support for a new programming language:

1. Create a new directory under the root (e.g., `go/`)
2. Implement the core functionality:
   - Cell parsing
   - Dependency resolution
   - Execution engine
   - Export functionality
   - HTML generation
3. Create documentation in the language-specific README
4. Add the language to the build workflow
5. Update this document with the new implementation

## Contributing

Contributions are welcome! Please follow the patterns established in existing implementations when adding new languages or features.