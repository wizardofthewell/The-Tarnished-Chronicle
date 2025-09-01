import subprocess
import os

def compile():
    print("Compiling resources...")
    
    # Path to the pyside6-rcc executable
    # This assumes venv is active or pyside6-rcc is in PATH
    rcc_executable = "pyside6-rcc"
    
    # Input and output file names
    qrc_file = "resources.qrc"
    py_file = "resources_rc.py"
    
    # Command to execute
    command = [rcc_executable, "-o", py_file, qrc_file]
    
    try:
        # Execute the command
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully compiled {qrc_file} to {py_file}")
    except FileNotFoundError:
        print(f"Error: '{rcc_executable}' not found.")
        print("Please ensure that PySide6 is installed and that its scripts directory is in your system's PATH, or run this from an activated venv.")
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation:")
        print(e.stderr)

if __name__ == "__main__":
    compile()