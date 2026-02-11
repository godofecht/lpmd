#!/usr/bin/env python3
"""
Literate Python Markdown (.lpmd) Executor

A new technology for executing literate programs written in markdown format.
Supports cell-based execution with dependencies, state persistence, and interactive elements.

Format:
--- cell:cell_id [depends:dep1,dep2] [persist:var1,var2] ---
```python
code here
```

Usage:
python lpmd_executor.py literate_python.md
"""

import re
import sys
import os
import subprocess
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass
import traceback

@dataclass
class Cell:
    id: str
    code: str
    dependencies: List[str]
    persist_vars: List[str]
    executed: bool = False
    output: str = ""
    error: str = ""

class LPMDExecutor:
    """Executor for Literate Python Markdown files"""

    def __init__(self):
        self.cells: Dict[str, Cell] = {}
        self.global_namespace: Dict[str, Any] = {}
        self.execution_order: List[str] = []

    def parse_lpmd_file(self, filepath: str) -> bool:
        """Parse a .lpmd file and extract cells with metadata"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
            return False

        # Split content by cell markers (both --- and <!-- --> syntax)
        cell_marker_pattern = r'--- cell:([^\s>]+)(.*?)---|<!-- cell:([^\s>]+)(.*?)-->'
        markers = re.findall(cell_marker_pattern, content)

        if not markers:
            print("❌ No cells found in .lpmd file")
            return False

        # Process each cell
        for marker in markers:
            # Handle both syntaxes (--- and <!-- -->)
            if marker[0]:  # --- syntax
                cell_id, metadata = marker[0], marker[1]
            else:  # <!-- --> syntax
                cell_id, metadata = marker[2], marker[3]

            # Find the corresponding code block
            # Look for the next ```python block after this marker
            marker_pos = content.find(f'<!-- cell:{cell_id}' if '<!--' in content else f'--- cell:{cell_id}')
            if marker_pos == -1:
                continue

            # Find the code block after the marker
            code_start = content.find('```python', marker_pos)
            if code_start == -1:
                continue

            code_start = content.find('\n', code_start) + 1  # Skip the ```python line
            code_end = content.find('```', code_start)
            if code_end == -1:
                continue

            code = content[code_start:code_end].strip()

            # Parse metadata
            dependencies = []
            persist_vars = []

            if metadata.strip():
                # Extract depends:cell1,cell2
                depends_match = re.search(r'depends:([^\s]+)', metadata)
                if depends_match:
                    dependencies = [d.strip() for d in depends_match.group(1).split(',')]

                # Extract persist:var1,var2
                persist_match = re.search(r'persist:([^\s]+)', metadata)
                if persist_match:
                    persist_vars = [v.strip() for v in persist_match.group(1).split(',')]

            # Create cell
            cell = Cell(
                id=cell_id,
                code=code,
                dependencies=dependencies,
                persist_vars=persist_vars
            )

            self.cells[cell_id] = cell

        print(f"📚 Parsed {len(self.cells)} cells from {filepath}")
        return True

    def resolve_execution_order(self) -> bool:
        """Resolve execution order based on dependencies using topological sort"""
        # Build dependency graph
        graph: Dict[str, Set[str]] = {cell_id: set(cell.dependencies) for cell_id, cell in self.cells.items()}
        in_degree: Dict[str, int] = {cell_id: len(cell.dependencies) for cell_id, cell in self.cells.items()}

        # Kahn's algorithm for topological sort
        queue = [cell_id for cell_id, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            current = queue.pop(0)
            result.append(current)

            # Find cells that depend on current (reverse edges don't exist, so we check all)
            for cell_id, deps in graph.items():
                if current in deps:
                    in_degree[cell_id] -= 1
                    if in_degree[cell_id] == 0:
                        queue.append(cell_id)

        if len(result) != len(self.cells):
            print("❌ Circular dependency detected or missing dependencies")
            return False

        self.execution_order = result
        print(f"🔄 Execution order resolved: {' → '.join(result)}")
        return True

    def execute_cell(self, cell: Cell) -> bool:
        """Execute a single cell and capture output"""
        print(f"\n{'='*60}")
        print(f"🎯 Executing Cell: {cell.id}")
        print('='*60)

        # Create local namespace with persisted variables
        local_namespace = self.global_namespace.copy()

        # Print code being executed
        print("Code:")
        print("-" * 40)
        for i, line in enumerate(cell.code.split('\n'), 1):
            print("2d")
        print("-" * 40)

        # Execute code
        try:
            print("Output:")
            print("-" * 40)

            # Capture stdout
            import io
            from contextlib import redirect_stdout

            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                exec(cell.code, local_namespace)

            cell.output = output_buffer.getvalue()
            print(cell.output)

            # Update global namespace with ALL variables from this cell
            # (not just persisted ones - dependencies need access to everything)
            self.global_namespace.update(local_namespace)

            # Show persisted variables if any
            if cell.persist_vars:
                persisted = [var for var in cell.persist_vars if var in local_namespace]
                if persisted:
                    print(f"💾 Explicitly persisted: {', '.join(persisted)}")

            cell.executed = True
            return True

        except Exception as e:
            error_msg = f"❌ Error in cell {cell.id}: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            cell.error = error_msg
            return False

    def execute_all(self) -> bool:
        """Execute all cells in dependency order"""
        print("🎵 Starting Literate Python Markdown Execution")
        print("=" * 55)

        success_count = 0
        for cell_id in self.execution_order:
            cell = self.cells[cell_id]

            # Check if all dependencies are satisfied
            missing_deps = [dep for dep in cell.dependencies if not self.cells[dep].executed]
            if missing_deps:
                print(f"❌ Cell {cell_id} missing dependencies: {missing_deps}")
                return False

            if self.execute_cell(cell):
                success_count += 1
            else:
                print(f"❌ Cell {cell_id} failed - stopping execution")
                return False

        print(f"\n{'='*60}")
        print("🎉 Literate Python Markdown Execution Complete!")
        print("=" * 60)
        print(f"✅ Successfully executed {success_count}/{len(self.cells)} cells")

        if success_count == len(self.cells):
            print("🎊 All cells executed successfully!")
            return True
        else:
            print(f"⚠️  {len(self.cells) - success_count} cells failed")
            return False

    def show_status(self):
        """Show execution status of all cells"""
        print("📊 Cell Execution Status:")
        print("=" * 40)

        for cell_id in self.execution_order:
            cell = self.cells[cell_id]
            status = "✅" if cell.executed else "⏳"
            deps = f" ← {','.join(cell.dependencies)}" if cell.dependencies else ""
            persist = f" → {','.join(cell.persist_vars)}" if cell.persist_vars else ""
            print("12")

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python lpmd_executor.py <filename.lpmd> [--yes]")
        print("Example: python lpmd_executor.py literate_python.md")
        print("         python lpmd_executor.py literate_python.md --yes")
        sys.exit(1)

    filepath = sys.argv[1]
    auto_confirm = len(sys.argv) == 3 and sys.argv[2] == "--yes"

    if not filepath.endswith('.lpmd') and not filepath.endswith('.md'):
        print("❌ File must have .lpmd or .md extension")
        sys.exit(1)

    executor = LPMDExecutor()

    # Parse file
    if not executor.parse_lpmd_file(filepath):
        sys.exit(1)

    # Resolve execution order
    if not executor.resolve_execution_order():
        sys.exit(1)

    # Show execution plan
    executor.show_status()

    # Ask for confirmation (unless --yes flag used)
    if not auto_confirm:
        try:
            response = input("\n🚀 Execute literate program? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("❌ Execution cancelled")
                sys.exit(0)
        except EOFError:
            print("❌ Non-interactive environment - use --yes flag")
            sys.exit(1)

    # Execute
    success = executor.execute_all()

    # Show final status
    print("\n📊 Final Execution Status:")
    executor.show_status()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
