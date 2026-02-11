# LitPro.js - Literate Programming Framework for JavaScript

LitPro.js brings the power of literate programming to the JavaScript ecosystem. Write executable documents that combine narrative text with JavaScript code, with explicit dependency management between code blocks.

## Features

- **Cell-Based Execution**: Code organized in executable cells with dependency management
- **Smart Dependencies**: Cells run in dependency order using topological sort
- **Markdown Native**: Uses markdown format with special cell markers
- **JavaScript Powered**: Full access to JavaScript's ecosystem and capabilities
- **Easy Export**: Export to plain JavaScript code or HTML documentation

## Installation

### Node.js
```bash
npm install litpro-js
```

### Browser
Include directly in your HTML:
```html
<script src="https://cdn.jsdelivr.net/npm/litpro-js@latest/LitPro.js"></script>
```

## Usage

### Node.js Usage

Create a literate programming file (e.g., `example.lit`):

```markdown
# My First Literate Program

<!-- cell:setup -->
```js
console.log("Hello from LitPro.js!");
let x = 10;
let y = 20;
```

<!-- cell:compute depends:setup -->
```js
let result = x + y;
console.log(`Sum: ${result}`);
```

<!-- cell:display depends:compute -->
```js
console.log(`The final result is: ${result}`);
```
```

Then execute it in Node.js:

```javascript
const LitPro = require('litpro-js');
const fs = require('fs');

const content = fs.readFileSync('example.lit', 'utf8');
const litpro = new LitPro();

await litpro.runLitPro(content);
```

### Browser Usage

```html
<script src="LitPro.js"></script>
<script>
  const litpro = new window.LitPro();
  
  const content = `<!-- cell:setup -->
\`\`\`js
console.log("Hello from LitPro.js in browser!");
let x = 10;
\`\`\`

<!-- cell:compute depends:setup -->
\`\`\`js
let result = x * 2;
console.log(\`Result: \${result}\`);
\`\`\``;
  
  litpro.runLitPro(content);
</script>
```

## Cell Syntax

LitPro.js uses HTML comments as cell markers to keep the markdown readable while enabling execution:

```markdown
<!-- cell:cell_id [depends:dep1,dep2] -->
```js
// Your JavaScript code here
code goes here
```
```

Parameters:
- `cell_id`: Unique identifier for the cell
- `depends`: Comma-separated list of cells this cell depends on

## API Reference

### Constructor
- `new LitPro()`: Create a new LitPro instance

### Methods
- `runLitPro(content)`: Execute literate programming content
- `exportLitPro(content, outputFile)`: Export to plain JavaScript code
- `htmlLitPro(content, outputFile)`: Generate HTML documentation
- `parseCells(content)`: Parse cells from content
- `resolveDependencies(cells)`: Resolve execution order

## Examples

### Basic Arithmetic

```markdown
<!-- cell:initialize -->
```js
let a = 5;
let b = 10;
console.log(`a = ${a}, b = ${b}`);
```

<!-- cell:calculate depends:initialize -->
```js
let result = a * b;
console.log(`Result: ${result}`);
```
```

### Web API Example

```markdown
<!-- cell:fetch-data -->
```js
async function fetchData() {
  try {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    console.log('Data received:', data);
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}
```

<!-- cell:process-data depends:fetch-data -->
```js
const data = await fetchData();
if (data) {
  const processed = data.map(item => ({ ...item, processed: true }));
  console.log('Processed data:', processed);
}
```
```

## How It Works

1. LitPro.js parses the file to identify cells and their dependencies
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