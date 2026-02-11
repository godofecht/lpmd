#!/usr/bin/env python3
"""
LPMD Standalone HTML Generator - Creates HTML that runs Python in the browser!

Uses Pyodide (WebAssembly Python interpreter) to execute Python code directly
in the browser without requiring a server.
"""

import re
import json
from typing import List, Dict, Any
from lpmd_executor import LPMDExecutor

class LPMDStandaloneHTMLGenerator:
    """Generate standalone HTML with embedded Pyodide for browser execution"""

    def __init__(self):
        self.cells = []
        self.metadata = {}
        self.source_file = None

    def parse_lpmd_file(self, filepath: str) -> bool:
        """Parse LPMD file using the existing executor"""
        self.source_file = filepath
        executor = LPMDExecutor()
        success = executor.parse_lpmd_file(filepath)
        if success:
            self.cells = executor.cells
            self.metadata = {'title': 'LPMD Document'}
        return success

    def split_markdown_content(self, filepath: str) -> List[str]:
        """Split markdown content by cells and extract text sections"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            return []

        # Simple approach: extract content before first cell and between major sections
        sections = []

        # Get content before first cell marker
        first_cell_pos = content.find('<!-- cell:')
        if first_cell_pos > 0:
            before_first = content[:first_cell_pos].strip()
            if before_first:
                sections.append(before_first)

        # For now, let's just include the main title and intro
        # This is a simplified version - in a full implementation we'd parse all sections
        if not sections:
            # Fallback: extract basic header content
            lines = content.split('\n')[:10]  # First 10 lines
            header_content = '\n'.join(lines).strip()
            if header_content:
                sections.append(header_content)

        return sections

    def generate_standalone_html(self, output_file: str) -> str:
        """Generate HTML with embedded Pyodide"""

        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Standalone LPMD</title>
    <style>
        {css}
    </style>
    <!-- Pyodide for Python execution in browser -->
    <script src="https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js"></script>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p class="subtitle">Standalone Literate Python Markdown</p>
            <div class="controls">
                <button onclick="initializePyodide()" id="init-btn" class="btn btn-primary">🚀 Initialize Python</button>
                <button onclick="executeAll()" id="execute-btn" class="btn btn-secondary" disabled>▶️ Execute All</button>
                <button onclick="clearAll()" class="btn btn-secondary">🗑️ Clear Output</button>
                <span class="status" id="status">Ready</span>
            </div>
        </header>

        <main id="content">
            {content}
        </main>
    </div>

    <script>
        {javascript}
    </script>
</body>
</html>"""

        css = self._generate_css()
        javascript = self._generate_javascript()

        # Generate content sections with interleaved markdown and cells
        content_html = ""

        # Get markdown sections from the source file
        markdown_sections = self.split_markdown_content(self.source_file)

        print(f"Found {len(markdown_sections)} markdown sections")

        # Add intro section
        content_html += '''
        <div class="markdown-section">
            <h2>🎵 Literate Python Markdown Demo</h2>
            <p>This is a <strong>standalone LPMD HTML file</strong> that combines documentation and executable code!</p>
            <p>Click "🚀 Initialize Python" to load Pyodide, then "▶️ Execute All" to run the code cells.</p>
            <p><em>Python executes directly in your browser - no server required!</em></p>
        </div>
        '''

        # Interleave markdown sections with cells
        cell_index = 0
        cells_list = list(self.cells.items())

        # Add the header/intro markdown if found
        for section in markdown_sections[:1]:  # Just the first section for now
            if section.strip():
                content_html += self._markdown_to_html(section)

        # Add cells with any markdown content that comes after each cell
        section_idx = 1
        for cell_index in range(len(cells_list)):
            cell_id, cell = cells_list[cell_index]
            content_html += self._generate_standalone_cell_html(cell, cell_index)

            # Add markdown section that comes after this cell (if any)
            if section_idx < len(markdown_sections):
                section = markdown_sections[section_idx]
                if section.strip():
                    content_html += self._markdown_to_html(section)
                section_idx += 1

        html_content = html_template.format(
            title=self.metadata.get('title', 'LPMD Document'),
            css=css,
            javascript=javascript,
            content=content_html
        )

        # Write HTML file
        with open(output_file, 'w') as f:
            f.write(html_content)

        return html_content

    def _generate_standalone_cell_html(self, cell, index: int) -> str:
        """Generate HTML for a standalone executable cell"""
        deps_info = f" ← {', '.join(cell.dependencies)}" if cell.dependencies else ""
        persist_info = f" → {', '.join(cell.persist_vars)}" if cell.persist_vars else ""

        return f'''
        <div class="cell" id="cell-{index}">
            <div class="cell-header">
                <span class="cell-id">Cell: {cell.id}</span>
                <span class="cell-meta">{deps_info} {persist_info}</span>
                <button onclick="executeCell({index})" class="btn btn-small" disabled>▶️ Run</button>
            </div>
            <div class="cell-input">
                <pre><code class="language-python" id="code-{index}">{cell.code}</code></pre>
            </div>
            <div class="cell-output" id="output-{index}" style="display: none;">
                <div class="output-header">Output:</div>
                <pre class="output-content" id="output-content-{index}"></pre>
            </div>
        </div>
        '''

    def _markdown_to_html(self, markdown: str) -> str:
        """Simple markdown to HTML converter"""
        import re

        html = markdown

        # Headers
        html = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

        # Bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

        # Code inline
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

        # Lists
        html = re.sub(r'^- (.*)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\n\1</ul>', html, flags=re.DOTALL)

        # Paragraphs
        paragraphs = []
        for para in html.split('\n\n'):
            if para.strip() and not para.startswith('<'):
                paragraphs.append(f'<p>{para}</p>')
            else:
                paragraphs.append(para)
        html = '\n\n'.join(paragraphs)

        return f'<div class="markdown-section">{html}</div>'

    def _generate_css(self) -> str:
        """Generate CSS with loading states"""
        base_css = '''
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
            min-height: 100vh;
        }

        header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 2rem;
            text-align: center;
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .controls {
            margin-top: 1.5rem;
            display: flex;
            justify-content: center;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .btn {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s;
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .btn-primary {
            background: #3498db;
            color: white;
        }

        .btn-primary:hover:not(:disabled) {
            background: #2980b9;
        }

        .btn-secondary {
            background: #95a5a6;
            color: white;
        }

        .btn-secondary:hover:not(:disabled) {
            background: #7f8c8d;
        }

        .btn-small {
            padding: 0.25rem 0.5rem;
            font-size: 0.8rem;
        }

        .status {
            font-weight: bold;
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
        }

        .status-ready {
            color: #28a745;
            background: rgba(40, 167, 69, 0.1);
        }

        .status-loading {
            color: #ffc107;
            background: rgba(255, 193, 7, 0.1);
        }

        .status-executing {
            color: #007bff;
            background: rgba(0, 123, 255, 0.1);
        }

        .status-success {
            color: #28a745;
            background: rgba(40, 167, 69, 0.1);
        }

        .status-error {
            color: #dc3545;
            background: rgba(220, 53, 69, 0.1);
        }

        main {
            padding: 2rem;
        }

        .markdown-section {
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }

        .markdown-section h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }

        .markdown-section p {
            margin-bottom: 1rem;
            line-height: 1.7;
        }

        .cell {
            border: 1px solid #e1e8ed;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            background: #fafbfc;
            overflow: hidden;
        }

        .cell-header {
            background: #f1f8ff;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #e1e8ed;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .cell-id {
            font-weight: bold;
            color: #0366d6;
        }

        .cell-meta {
            font-size: 0.9rem;
            color: #586069;
            font-style: italic;
        }

        .cell-input {
            background: white;
        }

        .cell-input pre {
            margin: 0;
            padding: 1rem;
            overflow-x: auto;
        }

        .cell-input code {
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9rem;
            line-height: 1.4;
        }

        .cell-output {
            background: #f6f8fa;
            border-top: 1px solid #e1e8ed;
        }

        .output-header {
            padding: 0.5rem 1rem;
            background: #e6f7ff;
            font-weight: bold;
            color: #005cc5;
        }

        .output-content {
            padding: 1rem;
            margin: 0;
            white-space: pre-wrap;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9rem;
            line-height: 1.4;
            color: #24292e;
        }

        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @media (max-width: 768px) {
            .container {
                margin: 0;
                border-radius: 0;
            }

            header {
                padding: 1rem;
            }

            .controls {
                flex-direction: column;
                gap: 0.5rem;
            }

            main {
                padding: 1rem;
            }

            .cell-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }
        }
        '''
        return base_css

    def _generate_javascript(self) -> str:
        """Generate JavaScript with Pyodide integration"""
        # Convert cells to dict format for JSON serialization
        cells_dict = []
        for cell_id, cell in self.cells.items():
            cells_dict.append({
                'id': cell.id,
                'code': cell.code,
                'dependencies': cell.dependencies,
                'persist_vars': cell.persist_vars
            })
        cells_data = json.dumps(cells_dict)

        # Build JavaScript as regular string to avoid f-string issues
        javascript = '''
        let pyodide = null;
        let isInitialized = false;
        const cells = ''' + cells_data + ''';

        function updateStatus(message, type = 'ready') {{
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = `status status-${{type}}`;
        }}

        async function initializePyodide() {{
            if (isInitialized) return;

            const btn = document.getElementById('init-btn');
            btn.textContent = '⏳ Loading Pyodide...';
            updateStatus('Loading Pyodide (this may take 10-30 seconds)...', 'loading');

            console.log('Starting Pyodide initialization...');

            try {{
                // Load Pyodide with updated URL and simpler config
                pyodide = await loadPyodide({{
                    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/"
                }});

                console.log('Pyodide loaded, testing Python...');

                // Simple test to ensure Python works
                const testResult = await pyodide.runPythonAsync('print("Python initialized successfully!"); 42');
                console.log('Python test successful:', testResult);

                isInitialized = true;
                btn.disabled = true;
                btn.textContent = '✅ Python Ready';
                document.getElementById('execute-btn').disabled = false;

                // Enable all cell buttons
                document.querySelectorAll('.btn-small').forEach(btn => {{
                    btn.disabled = false;
                }});

                updateStatus('Python Ready! Click Execute All to run code.', 'success');
                console.log('Pyodide initialization complete!');

            }} catch (error) {{
                console.error('Pyodide initialization failed:', error);
                btn.textContent = '❌ Failed';
                updateStatus('Failed to load Python: Check console for details', 'error');

                alert('Pyodide failed to load. Possible issues:\\n' +
                      '1. Slow internet connection (try again)\\n' +
                      '2. Network/firewall blocking CDN\\n' +
                      '3. Browser compatibility issues\\n\\n' +
                      'Check browser console (F12) for technical details.');
            }}
        }}

        async function executeCell(cellIndex) {{
            if (!isInitialized) {{
                alert('Please initialize Python first!');
                return;
            }}

            const cell = cells[cellIndex];
            const outputDiv = document.getElementById(`output-${{cellIndex}}`);
            const outputContent = document.getElementById(`output-content-${{cellIndex}}`);
            const button = document.querySelector(`#cell-${{cellIndex}} .btn-small`);

            button.disabled = true;
            button.textContent = '⏳ Running...';
            outputDiv.style.display = 'block';
            outputContent.textContent = 'Executing...';

            try {{
                // Execute code in Pyodide
                const code = cell.code;
                try {
                    // Simple execution - let print statements work naturally
                    const result = await pyodide.runPythonAsync(code);
                    // Display the result
                    outputContent.textContent = output;
                    button.textContent = '✅ Done';

            }} catch (error) {{
                outputContent.textContent = `Execution error: ${{error.message || error}}`;
                button.textContent = '❌ Error';
                console.error('Cell execution error:', error);
            }}

            button.disabled = false;
        }}

        async function executeAll() {{
            if (!isInitialized) {{
                alert('Please initialize Python first!');
                return;
            }}

            updateStatus('Executing all cells...', 'executing');
            document.getElementById('execute-btn').disabled = true;

            // Execute cells in order
            for (let i = 0; i < cells.length; i++) {{
                await executeCell(i);
                await new Promise(resolve => setTimeout(resolve, 500)); // Small delay
            }}

            updateStatus('All cells executed!', 'success');
            document.getElementById('execute-btn').disabled = false;
        }}

        function clearAll() {{
            document.querySelectorAll('.output-content').forEach(el => {{
                el.textContent = '';
                el.parentElement.style.display = 'none';
            }});

            document.querySelectorAll('.btn-small').forEach(btn => {{
                btn.textContent = '▶️ Run';
            }});

            updateStatus('Output cleared', 'ready');
        }}

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            updateStatus('Ready', '');
        });
        '''

        return javascript

def main():
    import sys

    if len(sys.argv) != 3:
        print("Usage: python lpmd_standalone_html.py input.lpmd output.html")
        print("Example: python lpmd_standalone_html.py literate_python.md standalone.html")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    generator = LPMDStandaloneHTMLGenerator()

    if not generator.parse_lpmd_file(input_file):
        sys.exit(1)

    generator.generate_standalone_html(output_file)
    print(f"✅ Generated standalone HTML: {output_file}")
    print(f"📊 Cells embedded: {len(generator.cells)}")
    print()
    print("🎉 This HTML file runs Python in your browser!")
    print("   Just open it and click 'Initialize Python' then 'Execute All'")
    print()
    print("🚀 No server required - pure browser-based execution!")

if __name__ == "__main__":
    main()
