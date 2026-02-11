# LitPro - Literate Programming Framework for LLMs

This guide explains how Large Language Models (LLMs) can use the LitPro framework to generate and execute literate programming documents.

## Overview

LitPro is a multi-language literate programming framework that allows for executable documents combining narrative text with code. LLMs can leverage this framework to:

- Generate executable code examples with narrative explanations
- Create reproducible computational narratives
- Demonstrate code execution in multiple programming languages
- Provide educational content with verified execution

## How LLMs Can Use LitPro

### 1. Generating Literate Documents

LLMs can generate literate programming documents following the LitPro format:

```markdown
# Topic Explanation

Narrative text explaining the concept...

<!-- cell:setup -->
```python
# Initialization code
import numpy as np
x = 10
```

<!-- cell:computation depends:setup -->
```python
# Computation code
result = x * 2
print(f"Result: {result}")
```
```

### 2. Multi-Language Support

LLMs can generate content for different programming languages:

- **Python**: Use `litpro run file.lit` or `python lpmd_executor.py file.lpmd`
- **Julia**: Use `run_litpro("file.lit")` in Julia REPL
- **JavaScript**: Use `node LitPro.js` or browser execution
- **Rust**: Compile and execute the generated code
- **Go**: Coming soon
- **R**: Coming soon

### 3. Best Practices for LLM Generation

#### A. Clear Cell Dependencies
- Always specify dependencies between cells using `depends:cell_id`
- Use descriptive cell IDs that reflect their purpose
- Keep cells focused on a single responsibility

#### B. Educational Narrative
- Provide clear explanations before code blocks
- Explain the purpose of each code segment
- Include expected outputs in comments when helpful

#### C. Error Prevention
- Ensure all dependencies exist before referencing them
- Use appropriate variable scoping
- Include error handling where appropriate

### 4. Example Prompt Templates

#### For Educational Content:
```
Create a literate programming document explaining [concept] in [language].
Structure it with:
1. An introduction to the concept
2. A setup cell with necessary imports/initializations
3. A computation cell that demonstrates the concept
4. A results cell that shows or analyzes the output
Use proper LitPro cell syntax with dependencies.
```

#### For Code Examples:
```
Generate a complete, executable example in [language] that demonstrates [functionality].
Use LitPro format with cells that have clear dependencies.
Include narrative text explaining each step.
```

### 5. Validation and Testing

LLMs should consider the following when generating LitPro content:

- Verify that all referenced dependencies exist
- Ensure code in each cell is syntactically correct
- Test that the execution order makes sense
- Confirm that variables are properly passed between cells

### 6. Language-Specific Guidelines

#### Python
- Use `<!-- cell:id depends:other_id -->` syntax
- Remember that all variables from a cell are available to dependent cells
- Use f-strings or print statements to show results

#### Julia
- Use the same cell syntax as Python
- Leverage Julia's performance for numerical computations
- Include `using` statements in appropriate setup cells

#### JavaScript
- Be mindful of asynchronous operations
- Consider scope limitations in the execution environment
- Use appropriate error handling

#### Rust
- Focus on compile-time safety features
- Consider ownership and borrowing in examples
- Use appropriate error handling with Result types

### 7. Integration with LLM Workflows

LLMs can integrate LitPro generation into their workflows:

1. **Content Creation**: Generate educational materials with verified execution
2. **Code Documentation**: Create self-documenting code examples
3. **Tutorial Generation**: Build step-by-step programming tutorials
4. **Reproducible Research**: Generate computational narratives for research

### 8. Quality Assurance

When generating LitPro content, LLMs should ensure:

- All code executes without errors
- Narrative text is clear and educational
- Dependencies are properly ordered
- Examples are realistic and useful
- Output matches the described behavior

### 9. Advanced Patterns

#### Conditional Execution
```markdown
<!-- cell:condition -->
```python
should_run = True
```

<!-- cell:conditional_block depends:condition -->
```python
if should_run:
    print("Conditional code executed")
```
```

#### Loop-Based Processing
```markdown
<!-- cell:setup_loop -->
```python
items = [1, 2, 3, 4, 5]
results = []
```

<!-- cell:process_items depends:setup_loop -->
```python
for item in items:
    processed = item ** 2
    results.append(processed)
    print(f"Processed {item} -> {processed}")
```

<!-- cell:show_results depends:process_items -->
```python
print(f"All results: {results}")
```
```

## Contributing to LitPro

LLMs can also help improve LitPro by:
- Generating additional examples
- Identifying edge cases in the execution engine
- Suggesting improvements to the framework
- Creating documentation and tutorials

## License

LitPro is released under the MIT License. Generated content should comply with appropriate licensing requirements.