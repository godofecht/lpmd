"""
LitPro Command-Line Interface

Provides the 'litpro' command with subcommands for running, exporting, and generating HTML.
"""

import argparse
import sys
import os
from pathlib import Path

def run_command(args):
    """Execute a literate programming file."""
    from core.lpmd_executor import LPMDExecutor
    
    if not args.file.endswith(('.lit', '.lpmd', '.md')):
        print(f"Error: File must have .lit, .lpmd, or .md extension")
        sys.exit(1)
    
    executor = LPMDExecutor()
    
    if not executor.parse_lpmd_file(args.file):
        sys.exit(1)
    
    if not executor.resolve_execution_order():
        sys.exit(1)
    
    # Auto-confirm execution
    success = executor.execute_all()
    sys.exit(0 if success else 1)

def export_command(args):
    """Export a literate programming file to plain code."""
    print(f"Exporting {args.file} to plain code...")
    # Implementation would go here
    print("Export functionality coming soon.")

def html_command(args):
    """Generate HTML documentation from a literate programming file."""
    from core.lpmd_html_generator import generate_html
    
    if not args.file.endswith(('.lit', '.lpmd', '.md')):
        print(f"Error: File must have .lit, .lpmd, or .md extension")
        sys.exit(1)
    
    # Read the file
    with open(args.file, 'r') as f:
        content = f.read()
    
    # Generate HTML
    html_content = generate_html(content)
    
    # Determine output filename
    input_path = Path(args.file)
    output_file = input_path.with_suffix('.html')
    
    # Write HTML output
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"HTML documentation generated: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='LitPro - Literate Programming Framework')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Execute a literate programming file')
    run_parser.add_argument('file', help='Path to the literate programming file (.lit, .lpmd, or .md)')
    run_parser.add_argument('--yes', action='store_true', help='Auto-confirm execution without prompts')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export to plain code')
    export_parser.add_argument('file', help='Path to the literate programming file (.lit, .lpmd, or .md)')
    
    # HTML command
    html_parser = subparsers.add_parser('html', help='Generate HTML documentation')
    html_parser.add_argument('file', help='Path to the literate programming file (.lit, .lpmd, or .md)')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        run_command(args)
    elif args.command == 'export':
        export_command(args)
    elif args.command == 'html':
        html_command(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()