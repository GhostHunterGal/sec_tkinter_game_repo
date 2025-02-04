# -*- coding: utf-8 -*-
import os
import subprocess
import sys

# Function to execute shell commands safely
def execute_command(command, error_message):
    """Executes a shell command and exits if it fails."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"❌ {error_message}\nError: {error.decode('utf-8')}")
        sys.exit(1)  # Exit the script on failure
    return output.decode("utf-8").strip()

# Step 1: Verify Git Installation
if not execute_command("git --version", "Git is not installed. Please install Git and rerun the script."):
    sys.exit(1)

# Step 2: Rename `cardGame.py` to `main.py`
if os.path.exists("cardGame.py"):
    os.rename("cardGame.py", "main.py")
    print("✅ Renamed `cardGame.py` to `main.py`.")
else:
    print("❌ `cardGame.py` not found! Ensure you're running this script in the correct folder.")
    sys.exit(1)

# Step 3: Create Directory Structure
os.makedirs("sec_game", exist_ok=True)
os.makedirs("tkinter_fix_scripts", exist_ok=True)

# Move the game script into `/sec_game/`
if os.path.exists("main.py"):
    os.rename("main.py", os.path.join("sec_game", "main.py"))
    print("✅ Moved `main.py` into `sec_game/`.")

# Move the Tkinter fix script
if os.path.exists("fix_tkinter.py"):
    os.rename("fix_tkinter.py", os.path.join("tkinter_fix_scripts", "fix_tkinter.py"))
    print("✅ Moved `fix_tkinter.py` into `tkinter_fix_scripts/`.")

# Step 4: Create `requirements.txt`
requirements_content = "tk\n"
with open("sec_game/requirements.txt", "w") as req_file:
    req_file.write(requirements_content)
print("✅ Created `requirements.txt` in `sec_game/`.")

# Step 5: Create `.gitignore`
gitignore_content = """
# Ignore Python cache files
__pycache__/
*.pyc
*.pyo

# Ignore VS Code settings
.vscode/

# Ignore macOS system files
.DS_Store

# Ignore environment files
.env
venv/
"""
with open(".gitignore", "w") as gitignore_file:
    gitignore_file.write(gitignore_content)
print("✅ Created `.gitignore`.")

# Step 6: Initialize Git Repository
if not os.path.exists(".git"):
    execute_command("git init", "Failed to initialize Git repository.")
    print("✅ Git repository initialized.")

# Step 7: Add & Commit Changes
execute_command("git add .", "Failed to stage files for commit.")
execute_command('git commit -m "Initial commit - SEC Football Card Game + Tkinter Fix"', "Failed to commit changes.")
print("✅ Git commit created.")

# Step 8: Set Up GitHub Remote & Push (User must update repo URL)
GITHUB_REPO_URL = "https://github.com/ghosthuntergal/sec_tkinter_game_repo.git"  # Change this!
execute_command(f"git remote add origin {GITHUB_REPO_URL}", "Failed to set remote GitHub repository.")
execute_command("git branch -M main", "Failed to rename branch to `main`.")
execute_command("git push -u origin main", "Failed to push to GitHub.")
print("✅ Successfully pushed to GitHub!")

# Final Instructions
print("\n🎉 **Setup Complete!** You can now open your GitHub repo to verify everything.")
