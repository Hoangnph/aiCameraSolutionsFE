#!/usr/bin/env python3
"""
📋 List All Scripts
Script để liệt kê tất cả các script có sẵn
"""

import os
import glob

def list_scripts():
    """List all Python scripts in current directory"""
    print("📋 Available Scripts in Face Detection System")
    print("=" * 60)
    
    # Get all .py files
    scripts = glob.glob("*.py")
    scripts.sort()
    
    if not scripts:
        print("❌ No Python scripts found!")
        return
    
    print(f"Found {len(scripts)} script(s):\n")
    
    for i, script in enumerate(scripts, 1):
        # Read first few lines to get description
        try:
            with open(script, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                description = ""
                for line in lines[:5]:  # Check first 5 lines
                    if '"""' in line or "'''" in line:
                        # Extract description from docstring
                        if '"""' in line:
                            desc = line.split('"""')[1] if '"""' in line else ""
                        else:
                            desc = line.split("'''")[1] if "'''" in line else ""
                        if desc.strip():
                            description = desc.strip()
                            break
                
                # Check if executable
                is_executable = os.access(script, os.X_OK)
                exec_status = "✅" if is_executable else "❌"
                
                print(f"{i:2d}. {exec_status} {script}")
                if description:
                    print(f"    📝 {description}")
                print()
                
        except Exception as e:
            print(f"{i:2d}. ❌ {script} (Error reading: {e})")
            print()

def show_quick_commands():
    """Show quick commands for common tasks"""
    print("🎯 Quick Commands")
    print("=" * 30)
    
    commands = [
        ("🚀 Start Frontend", "python quick_start_fe.py"),
        ("🛑 Stop Frontend", "python stop_frontend.py"),
        ("📊 Check Status", "python manage_frontend.py status"),
        ("🔄 Restart Frontend", "python manage_frontend.py restart"),
        ("🚀 Start Backend", "python start_backend.py"),
        ("🛑 Stop All", "python stop_all.py"),
        ("🚀 Start All", "python start_all.py"),
    ]
    
    for desc, cmd in commands:
        print(f"{desc:20} {cmd}")
    
    print()

def show_urls():
    """Show access URLs"""
    print("🌐 Access URLs")
    print("=" * 20)
    print("Frontend: http://localhost:3000")
    print("Backend:  http://localhost:8000")
    print()

def main():
    print("📋 Face Detection System - Scripts Overview")
    print("=" * 60)
    
    # List all scripts
    list_scripts()
    
    # Show quick commands
    show_quick_commands()
    
    # Show URLs
    show_urls()
    
    print("💡 Tips:")
    print("- Use 'python script_name.py' to run any script")
    print("- Use 'chmod +x script_name.py' to make script executable")
    print("- Use 'Ctrl+C' to stop running scripts")
    print("- Check FRONTEND_SCRIPTS.md for detailed documentation")

if __name__ == "__main__":
    main() 