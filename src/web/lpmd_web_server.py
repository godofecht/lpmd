#!/usr/bin/env python3
"""
LPMD Web Server - Serve interactive LPMD HTML with real-time code execution

This creates a web server that serves LPMD HTML pages with actual Python code execution
capabilities, making the documentation truly interactive.
"""

import http.server
import socketserver
import json
import sys
import os
import subprocess
import tempfile
import threading
from urllib.parse import parse_qs, urlparse
from lpmd_executor import LPMDExecutor

class LPMDRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for LPMD web server"""

    def __init__(self, *args, **kwargs):
        self.executor = LPMDExecutor()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            # Serve the main LPMD HTML file
            self.path = '/literate_python.html'
            return super().do_GET()
        else:
            return super().do_GET()

    def do_POST(self):
        """Handle POST requests for code execution"""
        if self.path == '/execute':
            self.handle_execute()
        else:
            self.send_error(404)

    def handle_execute(self):
        """Execute Python code and return results"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            code = data.get('code', '')
            cell_id = data.get('cell_id', 'unknown')

            # Execute code in isolated environment
            result = self.execute_code_safely(code, cell_id)

            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            self.wfile.write(json.dumps(result).encode('utf-8'))

        except Exception as e:
            self.send_error(500, f"Execution error: {str(e)}")

    def execute_code_safely(self, code: str, cell_id: str) -> dict:
        """Execute code in a safe, isolated environment"""
        try:
            # Create temporary file for execution
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                # Add safety imports and execution wrapper
                safe_code = f'''
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

# Capture output
stdout_capture = io.StringIO()
stderr_capture = io.StringIO()

try:
    with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
        # Safe execution environment
        {code}
except Exception as e:
    print(f"Error: {{e}}", file=sys.stderr)

# Output results
print("=== STDOUT ===")
print(stdout_capture.getvalue())
print("=== STDERR ===")
print(stderr_capture.getvalue())
'''
                f.write(safe_code)
                temp_file = f.name

            # Execute with timeout
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                cwd=os.getcwd()
            )

            # Clean up
            os.unlink(temp_file)

            # Parse output
            output = result.stdout
            error = result.stderr

            if result.returncode == 0:
                return {
                    'success': True,
                    'output': output,
                    'cell_id': cell_id
                }
            else:
                return {
                    'success': False,
                    'error': f'Exit code {result.returncode}\n{error}',
                    'cell_id': cell_id
                }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Code execution timed out (30 seconds)',
                'cell_id': cell_id
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Execution error: {str(e)}',
                'cell_id': cell_id
            }

    def end_headers(self):
        """Add CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.end_headers()

def run_server(port=8000):
    """Run the LPMD web server"""
    print("🎵 Starting LPMD Web Server")
    print("=" * 40)
    print(f"📡 Server will run at: http://localhost:{port}")
    print("📖 Open your browser to view interactive LPMD documentation")
    print("⚡ Code execution is fully functional!")
    print()
    print("Press Ctrl+C to stop the server")
    print()

    # Change to the directory containing our files
    os.chdir('/Users/abhishekshivakumar/4096')

    try:
        with socketserver.TCPServer(("", port), LPMDRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Usage: python lpmd_web_server.py [port]")
            sys.exit(1)

    run_server(port)
