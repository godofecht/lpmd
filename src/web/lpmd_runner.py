from flask import Flask, request, jsonify
import tempfile
import subprocess
import os
import sys
from pathlib import Path

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_lpmd():
    """
    Execute LPMD code using the actual Python interpreter
    """
    try:
        # Get the LPMD code from the request
        lpmd_code = request.json.get('code', '')
        
        if not lpmd_code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Create a temporary .lpmd file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.lpmd', delete=False) as f:
            f.write(lpmd_code)
            temp_filename = f.name
        
        try:
            # Execute the LPMD file using the actual LPMD executor
            # Assuming the executor is in the src/core directory
            executor_path = Path(__file__).parent.parent / 'src' / 'core' / 'lpmd_executor.py'
            
            # Run the executor with the temporary file
            result = subprocess.run([
                sys.executable, str(executor_path), temp_filename, '--yes'
            ], capture_output=True, text=True, timeout=30)
            
            # Combine stdout and stderr for output
            output = result.stdout
            if result.stderr:
                output += '\nSTDERR:\n' + result.stderr
            
            return jsonify({
                'success': result.returncode == 0,
                'output': output,
                'returncode': result.returncode
            })
            
        finally:
            # Clean up the temporary file
            os.unlink(temp_filename)
            
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Execution timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)