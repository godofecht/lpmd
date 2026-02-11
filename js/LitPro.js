// LitPro.js
// Literate Programming Framework for JavaScript

class LitPro {
  constructor() {
    this.cells = {};
    this.globalContext = {};
  }

  /**
   * Parse cells from literate programming content
   */
  parseCells(content) {
    const cellPattern = /<!--\s*cell:([^\s>]+)([^>]*)?-->[\s\n]*```(js|javascript)([\s\S]*?)```/gi;
    const cells = {};
    let match;

    while ((match = cellPattern.exec(content)) !== null) {
      const cellId = match[1].trim();
      const depsStr = match[2];
      const code = match[4].trim();

      // Parse dependencies
      const dependencies = [];
      if (depsStr) {
        const depsMatch = depsStr.match(/depends:([^\s]+)/);
        if (depsMatch) {
          dependencies.push(...depsMatch[1].split(',').map(dep => dep.trim()));
        }
      }

      cells[cellId] = {
        id: cellId,
        code: code,
        dependencies: dependencies,
        executed: false
      };
    }

    return cells;
  }

  /**
   * Resolve execution order using topological sort
   */
  resolveDependencies(cells) {
    const graph = {};
    const inDegree = {};

    // Initialize graph and in-degree
    Object.keys(cells).forEach(id => {
      graph[id] = [];
      inDegree[id] = 0;
    });

    // Build graph and calculate in-degrees
    Object.values(cells).forEach(cell => {
      cell.dependencies.forEach(dep => {
        if (cells[dep]) {  // Check if dependency exists
          graph[dep].push(cell.id);
          inDegree[cell.id]++;
        } else {
          console.warn(`Dependency ${dep} not found for cell ${cell.id}`);
        }
      });
    });

    // Kahn's algorithm for topological sort
    const queue = [];
    Object.keys(inDegree).forEach(node => {
      if (inDegree[node] === 0) {
        queue.push(node);
      }
    });

    const result = [];

    while (queue.length > 0) {
      const node = queue.shift();
      result.push(node);

      graph[node].forEach(neighbor => {
        inDegree[neighbor]--;
        if (inDegree[neighbor] === 0) {
          queue.push(neighbor);
        }
      });
    }

    // Check if all nodes were included (no cycles)
    if (result.length !== Object.keys(graph).length) {
      return null; // Cycle detected
    }

    return result;
  }

  /**
   * Execute a literate programming file
   */
  async runLitPro(content) {
    console.log("Executing literate file...");
    
    // Parse cells
    this.cells = this.parseCells(content);
    
    if (Object.keys(this.cells).length === 0) {
      console.log("No cells found in the literate file.");
      return;
    }

    // Resolve execution order
    const executionOrder = this.resolveDependencies(this.cells);
    
    if (!executionOrder) {
      throw new Error("Circular dependency detected in cells.");
    }

    console.log(`Found ${Object.keys(this.cells).length} cells with dependencies.`);
    console.log(`Execution order: ${executionOrder.join(' → ')}`);

    // Execute cells in order
    for (const cellId of executionOrder) {
      const cell = this.cells[cellId];
      
      console.log(`\n--- Executing cell: ${cell.id} ---`);
      if (cell.dependencies.length > 0) {
        console.log(`Dependencies: ${cell.dependencies.join(', ')}`);
      }
      
      try {
        // Create a function with the code and execute it in the global context
        const func = new Function(...Object.keys(this.globalContext), `"use strict";\n${cell.code}`);
        const result = func(...Object.values(this.globalContext));
        
        // Update global context with any new variables
        // Note: This is a simplified approach - in practice, you'd need more sophisticated variable tracking
        console.log("✓ Cell executed successfully");
        
        cell.executed = true;
      } catch (error) {
        console.error(`✗ Error in cell ${cell.id}:`, error);
        throw error;
      }
    }

    console.log("\n--- Execution completed ---");
  }

  /**
   * Export to plain JavaScript code
   */
  exportLitPro(content, outputFile) {
    const cells = this.parseCells(content);
    let exportedCode = "// Exported from LitPro\n\n";
    
    Object.entries(cells).forEach(([id, cell]) => {
      exportedCode += `// Cell: ${id}\n`;
      exportedCode += cell.code;
      exportedCode += "\n\n";
    });
    
    // In a real implementation, you'd write to the file system
    console.log("Exported code:");
    console.log(exportedCode);
    
    return exportedCode;
  }

  /**
   * Generate HTML documentation
   */
  htmlLitPro(content, outputFile) {
    const cells = this.parseCells(content);
    
    let htmlContent = `<!DOCTYPE html>
<html>
<head>
    <title>LitPro Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .cell { margin: 20px 0; padding: 15px; border-left: 3px solid #007acc; }
        .code { background: #f4f4f4; padding: 10px; border-radius: 4px; }
        pre { margin: 0; }
    </style>
</head>
<body>
    <h1>LitPro Documentation</h1>`;
    
    Object.entries(cells).forEach(([id, cell]) => {
      htmlContent += `
    <div class="cell">
        <h3>Cell: ${id}</h3>
        <div class="code">
            <pre><code class="language-javascript">${this.escapeHtml(cell.code)}</code></pre>
        </div>
    </div>`;
    });
    
    htmlContent += `
</body>
</html>`;
    
    // In a real implementation, you'd write to the file system
    console.log("Generated HTML:");
    console.log(htmlContent);
    
    return htmlContent;
  }

  /**
   * Escape HTML characters
   */
  escapeHtml(str) {
    return str.replace(/[&<>"']/g, 
      tag => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;'
      }[tag]));
  }
}

// Export for use in Node.js or browsers
if (typeof module !== 'undefined' && module.exports) {
  module.exports = LitPro;
} else if (typeof window !== 'undefined') {
  window.LitPro = LitPro;
}

// Example usage:
/*
const litpro = new LitPro();

const exampleContent = `
# My First Literate Program

<!-- cell:setup -->
\`\`\`js
console.log("Hello from LitPro.js!");
let x = 10;
let y = 20;
\`\`\`

<!-- cell:compute depends:setup -->
\`\`\`js
let result = x + y;
console.log(\`Sum: \${result}\`);
\`\`\`

<!-- cell:display depends:compute -->
\`\`\`js
console.log(\`The final result is: \${result}\`);
\`\`\`
`;

litpro.runLitPro(exampleContent);
*/