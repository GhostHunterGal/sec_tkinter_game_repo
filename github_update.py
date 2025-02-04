# -*- coding: utf-8 -*-
import subprocess
import sys

def execute_command(command, error_message, allow_continue=False):
    """Executes a shell command and exits if it fails (unless allow_continue=True)."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    
    output = output.decode("utf-8").strip()
    error = error.decode("utf-8").strip()
    
    if process.returncode != 0:
        if allow_continue and "non-fast-forward" in error:
            print(f"⚠️ {error_message}\nError details: {error}\nTrying force push...")
            return None  # Continue execution for force push
        print(f"❌ {error_message}\nError details: {error}")
        sys.exit(1)
    return output

# Step 1: Pull the latest changes first
execute_command("git pull --rebase origin main", "Failed to pull latest changes from GitHub.")

# Step 2: Try pushing normally
push_output = execute_command("git push origin main", "Failed to push changes to GitHub.", allow_continue=True)

# Step 3: If normal push fails, force push
if push_output is None:
    execute_command("git push --force origin main", "Failed to force push to GitHub.")
    print("✅ Force push successful.")

print("\n🎉 **Update Complete!** Your local branch is now synced with GitHub.")
