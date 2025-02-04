import subprocess
import os
import sys

def execute_command(command):
    """Executes a shell command and returns the output, error, and return code."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8'), process.returncode

def uninstall_python_tcltk():
    """Uninstalls potentially conflicting Python and Tcl/Tk installations via Homebrew."""
    print("🔧 Uninstalling potentially conflicting Python and Tcl/Tk versions...")
    commands = [
        "brew uninstall python3 --ignore-dependencies",
        "brew uninstall python-tk --ignore-dependencies",
        "brew uninstall python-tk@3.13 --ignore-dependencies",  # Specifically for 3.13
        "brew uninstall tcl-tk --ignore-dependencies",
    ]
    for command in commands:
        output, error, returncode = execute_command(command)
        if returncode != 0:
            print(f"Warning executing {command}: {error}")
        else:
            print(f"Successfully executed: {command}")

def install_tcltk_and_python_tk():
    """Installs Tcl/Tk and Python Tkinter bindings via Homebrew."""
    print("⬇️ Installing Tcl/Tk and Python Tkinter bindings...")
    commands = [
        "brew install tcl-tk",
        "brew install python-tk@3.13",  # Specifically for 3.13
    ]
    for command in commands:
        output, error, returncode = execute_command(command)
        if returncode != 0:
            print(f"Error executing {command}: {error}")
            sys.exit(1)  # Exit on error
        else:
            print(f"Successfully executed: {command}")
            print(f"Output:\n{output}")

def set_environment_variables():
    """Sets the TCL_LIBRARY and TK_LIBRARY environment variables."""
    print("=== Setting up environment variables ===")
    tcltk_prefix_cmd = "brew --prefix tcl-tk"
    tcltk_prefix_output, tcltk_prefix_error, tcltk_prefix_returncode = execute_command(tcltk_prefix_cmd)

    if tcltk_prefix_returncode == 0:
        tcltk_prefix = tcltk_prefix_output.strip()
        tcl_library_path = os.path.join(tcltk_prefix, "lib")
        tk_library_path = os.path.join(tcltk_prefix, "lib")

        print(f"🔧 Setting TCL_LIBRARY to {tcl_library_path}")
        print(f"🔧 Setting TK_LIBRARY to {tk_library_path}")

        # Add to shell configuration files
        with open(os.path.expanduser("~/.zshrc"), "a") as zshrc:
            zshrc.write(f"\nexport TCL_LIBRARY={tcl_library_path}\n")
            zshrc.write(f"export TK_LIBRARY={tk_library_path}\n")
        with open(os.path.expanduser("~/.bashrc"), "a") as bashrc:
            bashrc.write(f"\nexport TCL_LIBRARY={tcl_library_path}\n")
            bashrc.write(f"export TK_LIBRARY={tk_library_path}\n")

        # Export in current session
        os.environ["TCL_LIBRARY"] = tcl_library_path
        os.environ["TK_LIBRARY"] = tk_library_path

        print("✅ Environment variables written to ~/.zshrc and ~/.bashrc")
    else:
        print(f"Error getting tcl-tk prefix: {tcltk_prefix_error}")
        sys.exit(1)  # Exit on error

def verify_tkinter_installation():
    """Verifies if Tkinter is working correctly."""
    print("=== Verifying Tkinter installation ===")
    python_executable = "python3"  # Since we are using the default Python 3.13

    # Test Tkinter import and Tcl library detection
    tkinter_test_command = f'{python_executable} -c "import tkinter; print(tkinter.Tcl().eval(\'info library\'))"'
    tkinter_test_output, tkinter_test_error, tkinter_test_returncode = execute_command(tkinter_test_command)

    if tkinter_test_returncode == 0:
        print(f"✅ Tkinter is working correctly. Detected Tcl library path: {tkinter_test_output.strip()}")
    else:
        print(f"❌ Tkinter is still not available. Error: {tkinter_test_error}")
        sys.exit(1)  # Exit on error

    # Test Tkinter GUI
    tkinter_gui_command = f"{python_executable} -m tkinter"
    print("   (A Tkinter window should appear. Close it to continue.)")
    execute_command(tkinter_gui_command)

if __name__ == "__main__":
    print("=== Starting Tkinter fix script ===")
    uninstall_python_tcltk()
    install_tcltk_and_python_tk()
    set_environment_variables()
    verify_tkinter_installation()
    print("=== Tkinter fix script complete ===")
    print("✅ Please restart your terminal or source your shell configuration (e.g., source ~/.zshrc) for the changes to take effect.")