#!/usr/bin/env python3
"""
LPMD HTML Generator - Create beautiful HTML documentation from LPMD files

This generates HTML pages from LPMD markdown files with:
- Clean, modern design
- Syntax-highlighted code blocks
- Interactive cell execution buttons
- Real-time output display
- Responsive layout
"""

import re
import json
import os
from typing import List, Dict, Any
from datetime import datetime

class LPMDHTMLGenerator:
    """Generate HTML documentation from LPMD files"""

    def __init__(self):
        self.cells = []
        self.metadata = {}

    def parse_lpmd_file(self, filepath: str) -> bool:
        """Parse LPMD file and extract content"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
            return False

        # Extract title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        self.metadata['title'] = title_match.group(1).strip() if title_match else "LPMD Document"

        # Split content by cell markers
        cell_pattern = r'<!-- cell:([^\s>]+)(.*?) -->\s*\n```python\s*\n(.*?)\n```'
        matches = re.findall(cell_pattern, content, re.DOTALL)

        if not matches:
            print("❌ No LPMD cells found")
            return False

        # Parse cells
        for cell_id, metadata, code in matches:
            dependencies = []
            persist_vars = []

            if metadata.strip():
                depends_match = re.search(r'depends:([^\s]+)', metadata)
                if depends_match:
                    dependencies = [d.strip() for d in depends_match.group(1).split(',')]

                persist_match = re.search(r'persist:([^\s]+)', metadata)
                if persist_match:
                    persist_vars = [v.strip() for v in persist_match.group(1).split(',')]

            self.cells.append({
                'id': cell_id,
                'code': code.strip(),
                'dependencies': dependencies,
                'persist_vars': persist_vars
            })

        return True

    def split_markdown_content(self, filepath: str) -> List[str]:
        """Split markdown content by cells and extract text sections"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            return []

        # Split by cell markers and code blocks
        sections = []
        current_section = []

        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]

            # If we hit a cell marker or code block, save current section
            if line.startswith('<!-- cell:') or line.startswith('```python'):
                if current_section:
                    sections.append('\n'.join(current_section).strip())
                    current_section = []

                # Skip the cell content
                if line.startswith('<!-- cell:'):
                    # Skip until next section
                    while i < len(lines) and not (lines[i].strip() == '' and i + 1 < len(lines) and lines[i + 1].startswith('<!-- cell:')):
                        i += 1
                        if i < len(lines) and lines[i].startswith('<!-- cell:'):
                            i -= 1  # Back up to process this cell
                            break
                elif line.startswith('```python'):
                    # Skip code block
                    i += 1
                    while i < len(lines) and lines[i] != '```':
                        i += 1
                    i += 1  # Skip closing ```
            else:
                current_section.append(line)
                i += 1

        if current_section:
            sections.append('\n'.join(current_section).strip())

        return [s for s in sections if s.strip()]

    def generate_html(self, output_file: str) -> str:
        """Generate complete HTML page"""

        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - LPMD</title>
    <style>
        {css}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p class="subtitle">Interactive Literate Python Markdown</p>
            <div class="controls">
                <button onclick="executeAll()" class="btn btn-primary">▶️ Execute All</button>
                <button onclick="clearAll()" class="btn btn-secondary">🗑️ Clear Output</button>
                <span class="status">Ready</span>
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

        # Generate content sections
        content_sections = self.split_markdown_content(output_file.replace('.html', '.md'))
        content_html = ""

        cell_index = 0
        for section in content_sections:
            if section.strip():
                content_html += self._markdown_to_html(section)

                # Add cell if available
                if cell_index < len(self.cells):
                    cell = self.cells[cell_index]
                    content_html += self._generate_cell_html(cell, cell_index)
                    cell_index += 1

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

    def _markdown_to_html(self, markdown: str) -> str:
        """Simple markdown to HTML converter"""
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

    def _generate_cell_html(self, cell: Dict[str, Any], index: int) -> str:
        """Generate HTML for a code cell"""
        deps_info = f" ← {', '.join(cell['dependencies'])}" if cell['dependencies'] else ""
        persist_info = f" → {', '.join(cell['persist_vars'])}" if cell['persist_vars'] else ""

        return f'''
        <div class="cell" id="cell-{index}">
            <div class="cell-header">
                <span class="cell-id">Cell: {cell['id']}</span>
                <span class="cell-meta">{deps_info} {persist_info}</span>
                <button onclick="executeCell({index})" class="btn btn-small">▶️ Run</button>
            </div>
            <div class="cell-input">
                <pre><code class="language-python">{cell['code']}</code></pre>
            </div>
            <div class="cell-output" id="output-{index}" style="display: none;">
                <div class="output-header">Output:</div>
                <pre class="output-content"></pre>
            </div>
        </div>
        '''

    def _generate_css(self) -> str:
        """Generate CSS styles"""
        return '''
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
        }

        .btn {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.2s;
        }

        .btn-primary {
            background: #3498db;
            color: white;
        }

        .btn-primary:hover {
            background: #2980b9;
        }

        .btn-secondary {
            background: #95a5a6;
            color: white;
        }

        .btn-secondary:hover {
            background: #7f8c8d;
        }

        .btn-small {
            padding: 0.25rem 0.5rem;
            font-size: 0.8rem;
        }

        .status {
            font-weight: bold;
        }

        main {
            padding: 2rem;
        }

        .markdown-section {
            margin-bottom: 2rem;
        }

        .markdown-section h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }

        .markdown-section h2 {
            color: #34495e;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        .markdown-section h3 {
            color: #34495e;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }

        .markdown-section p {
            margin-bottom: 1rem;
            line-height: 1.7;
        }

        .markdown-section ul {
            margin-left: 2rem;
            margin-bottom: 1rem;
        }

        .markdown-section li {
            margin-bottom: 0.5rem;
        }

        .markdown-section code {
            background: #f8f9fa;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9em;
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
        }

        .status-executing {
            color: #fb8532;
        }

        .status-success {
            color: #28a745;
        }

        .status-error {
            color: #d73a49;
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

    def _generate_javascript(self) -> str:
        """Generate JavaScript for interactive functionality"""
        return f'''
        const cells = {json.dumps(self.cells)};
        let executionQueue = [];
        let isExecuting = false;

        function updateStatus(message, type = '') {{
            const status = document.querySelector('.status');
            status.textContent = message;
            status.className = `status ${{type}}`;
        }}

        async function executeCell(cellIndex) {{
            if (isExecuting) return;

            const cell = cells[cellIndex];
            const outputDiv = document.getElementById(`output-${{cellIndex}}`);
            const outputContent = outputDiv.querySelector('.output-content');

            updateStatus(`Executing cell: ${{cell.id}}`, 'status-executing');
            outputDiv.style.display = 'block';
            outputContent.textContent = 'Running...';

            try {{
                // Send code to Python backend for execution
                const response = await fetch('/execute', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        code: cell.code,
                        cell_id: cell.id,
                        dependencies: cell.dependencies
                    }})
                }});

                const result = await response.json();

                if (result.success) {{
                    outputContent.textContent = result.output;
                    updateStatus(`Cell ${{cell.id}} completed`, 'status-success');
                }} else {{
                    outputContent.textContent = `Error: ${{result.error}}`;
                    updateStatus(`Cell ${{cell.id}} failed`, 'status-error');
                }}

            }} catch (error) {{
                outputContent.textContent = `Network error: ${{error.message}}`;
                updateStatus(`Cell ${{cell.id}} failed`, 'status-error');
            }}
        }}

        async function executeAll() {{
            if (isExecuting) return;

            updateStatus('Executing all cells...', 'status-executing');
            isExecuting = true;

            // Simple execution order (in document order)
            for (let i = 0; i < cells.length; i++) {{
                await executeCell(i);
                await new Promise(resolve => setTimeout(resolve, 500)); // Small delay
            }}

            updateStatus('All cells executed', 'status-success');
            isExecuting = false;
        }}

        function clearAll() {{
            document.querySelectorAll('.output-content').forEach(el => {{
                el.textContent = '';
                el.parentElement.style.display = 'none';
            }});
            updateStatus('Output cleared', '');
        }}

        // Initialize syntax highlighting (if Prism.js available)
        document.addEventListener('DOMContentLoaded', function() {{
            updateStatus('Ready to execute cells', '');
        }});
        '''

def main():
    import sys

    if len(sys.argv) != 3:
        print("Usage: python lpmd_html_generator.py input.lpmd output.html")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    generator = LPMDHTMLGenerator()

    if not generator.parse_lpmd_file(input_file):
        sys.exit(1)

    generator.generate_html(output_file)
    print(f"✅ Generated HTML: {output_file}")
    print(f"📊 Cells found: {len(generator.cells)}")
    print(f"📖 Open {output_file} in your browser to see the interactive documentation!")

if __name__ == "__main__":
    main()
