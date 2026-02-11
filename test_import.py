# Test script to verify the LPMD package works correctly
import sys
import os

# Add the src directory to the path to test importing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Try to import the main module
    from core.lpmd_executor import LPMDExecutor, __version__
    
    print(f"✅ Successfully imported LPMDExecutor")
    print(f"✅ Version: {__version__}")
    
    # Create an executor instance
    executor = LPMDExecutor()
    print(f"✅ Successfully created LPMDExecutor instance")
    
    # Check that it has the expected methods
    expected_methods = ['parse_lpmd_file', 'resolve_execution_order', 'execute_cell', 'execute_all']
    for method in expected_methods:
        if hasattr(executor, method):
            print(f"✅ Method '{method}' exists")
        else:
            print(f"❌ Method '{method}' missing")
    
    print("\n🎉 LPMD package structure is correct and importable!")
    
except ImportError as e:
    print(f"❌ Failed to import LPMD: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error testing LPMD: {e}")
    sys.exit(1)