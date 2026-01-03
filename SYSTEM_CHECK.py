#!/usr/bin/env python
"""
Comprehensive System Check Script for MisMatch
Run: python SYSTEM_CHECK.py

Quickly diagnoses all system components and reports issues
"""

import sys
import subprocess
import platform
import os
from datetime import datetime

# Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Global counters
checks_passed = 0
checks_failed = 0
checks_warning = 0
failed_checks = []

def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{text}{Colors.END}")
    print(Colors.BLUE + "=" * 60 + Colors.END)

def print_success(text):
    """Print success message"""
    global checks_passed
    print(f"{Colors.GREEN}✓{Colors.END} {text}")
    checks_passed += 1

def print_error(text):
    """Print error message"""
    global checks_failed
    print(f"{Colors.RED}✗{Colors.END} {text}")
    checks_failed += 1
    failed_checks.append(text)

def print_warning(text):
    """Print warning message"""
    global checks_warning
    print(f"{Colors.YELLOW}⚠{Colors.END} {text}")
    checks_warning += 1

def run_command(command, show_output=False):
    """Run shell command and return success/failure"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        if show_output:
            return result.returncode == 0, result.stdout.strip()
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        return False

def check_command_exists(command, name):
    """Check if a command exists and is accessible"""
    success, output = run_command(f"{command} --version", show_output=True)
    if success:
        print_success(f"{name}: {output}")
        return True
    else:
        print_error(f"{name}: NOT INSTALLED or not in PATH")
        return False

def check_python_module(module_name, import_name=None):
    """Check if a Python module is installed"""
    if import_name is None:
        import_name = module_name
    
    success, output = run_command(
        f"python -c \"import {import_name}; print(getattr({import_name}, '__version__', 'installed'))\" 2>/dev/null",
        show_output=True
    )
    
    if success:
        print_success(f"{module_name}: {output}")
        return True
    else:
        print_error(f"{module_name}: NOT INSTALLED")
        return False

def check_port_available(port):
    """Check if port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    
    if result == 0:
        print_warning(f"Port {port}: ALREADY IN USE (another process is using it)")
        return False
    else:
        print_success(f"Port {port}: AVAILABLE")
        return True

def check_file_exists(filepath, name):
    """Check if file exists"""
    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        print_success(f"{name}: EXISTS ({size} bytes)")
        return True
    else:
        print_error(f"{name}: MISSING at {filepath}")
        return False

def check_directory_exists(dirpath, name):
    """Check if directory exists"""
    if os.path.isdir(dirpath):
        print_success(f"{name}: EXISTS")
        return True
    else:
        print_error(f"{name}: MISSING at {dirpath}")
        return False

def check_flask_app():
    """Check if Flask app loads without errors"""
    success, output = run_command(
        "python -c \"from app import app; print('Flask app loaded successfully')\"",
        show_output=True
    )
    
    if success:
        print_success("Flask app loads: OK")
        return True
    else:
        print_error(f"Flask app loads: FAILED - {output}")
        return False

def check_venv_active():
    """Check if virtual environment is active"""
    venv_path = sys.prefix
    
    if 'venv' in venv_path or 'virtualenv' in venv_path:
        print_success(f"Virtual environment: ACTIVE ({venv_path})")
        return True
    else:
        print_warning(f"Virtual environment: NOT ACTIVE (using {venv_path})")
        return False

def main():
    """Run all diagnostic checks"""
    
    # Header
    print(f"\n{Colors.CYAN}{Colors.BOLD}" + "="*60)
    print(f"🔍 MisMatch System Diagnostics")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"OS: {platform.system()} {platform.release()}")
    print("="*60 + Colors.END)
    
    # Phase 1: System Information
    print_header("📊 Phase 1: System Information")
    print(f"Platform: {platform.system()} {platform.version()}")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    
    # Phase 2: Virtual Environment
    print_header("🔧 Phase 2: Virtual Environment")
    check_venv_active()
    check_command_exists("pip", "pip")
    
    # Phase 3: Python Packages
    print_header("📦 Phase 3: Python Packages")
    flask_ok = check_python_module("Flask", "flask")
    check_python_module("Flask-CORS", "flask_cors")
    check_python_module("Flask-SQLAlchemy", "flask_sqlalchemy")
    check_python_module("SQLAlchemy", "sqlalchemy")
    check_python_module("psycopg2", "psycopg2")
    check_python_module("requests")
    
    # Phase 4: Project Files
    print_header("📁 Phase 4: Project Files")
    check_file_exists("app.py", "app.py")
    check_file_exists("requirements.txt", "requirements.txt")
    check_file_exists("Dockerfile", "Dockerfile")
    check_file_exists("docker-compose.yml", "docker-compose.yml")
    check_directory_exists("app", "app/ directory")
    check_directory_exists(".git", ".git/ directory")
    
    # Phase 5: Flask Application
    print_header("🚀 Phase 5: Flask Application")
    if flask_ok:
        check_flask_app()
    else:
        print_error("Flask app: CANNOT CHECK (Flask not installed)")
    
    # Phase 6: Port Availability
    print_header("🔌 Phase 6: Port Availability")
    check_port_available(5000)
    check_port_available(3000)
    check_port_available(5432)
    check_port_available(6379)
    
    # Phase 7: Docker
    print_header("🐳 Phase 7: Docker & Containers")
    if check_command_exists("docker", "Docker"):
        if check_file_exists("Dockerfile", "Dockerfile"):
            success = run_command("docker build -t mismatch:check . --quiet")
            if success:
                print_success("Docker build: OK (image built successfully)")
            else:
                print_warning("Docker build: Could not build (Dockerfile might be invalid)")
    
    check_command_exists("docker-compose", "Docker Compose")
    
    # Phase 8: Git
    print_header("📝 Phase 8: Git Version Control")
    check_command_exists("git", "Git")
    
    if os.path.isdir(".git"):
        success, output = run_command("git rev-parse --is-inside-work-tree", show_output=True)
        if success:
            print_success("Git repository: INITIALIZED")
            
            # Get branch
            _, branch = run_command("git rev-parse --abbrev-ref HEAD", show_output=True)
            if branch:
                print_success(f"Current branch: {branch}")
            
            # Get commit count
            _, commit_count = run_command("git rev-list --all --count", show_output=True)
            if commit_count:
                print_success(f"Total commits: {commit_count}")
    
    # Phase 9: Network Connectivity
    print_header("🌐 Phase 9: Network Connectivity")
    
    success = run_command("python -c \"import socket; socket.create_connection(('8.8.8.8', 53), timeout=2)\" 2>/dev/null")
    if success:
        print_success("Internet connectivity: OK")
    else:
        print_warning("Internet connectivity: Cannot reach external network")
    
    # Phase 10: Diagnostic Summary
    print_header("📊 Phase 10: Diagnostic Summary")
    
    total = checks_passed + checks_failed + checks_warning
    
    print(f"{Colors.GREEN}✓ Passed:  {checks_passed}/{total}{Colors.END}")
    print(f"{Colors.YELLOW}⚠ Warning: {checks_warning}/{total}{Colors.END}")
    print(f"{Colors.RED}✗ Failed:  {checks_failed}/{total}{Colors.END}")
    
    # Final status
    print("\n" + "="*60)
    
    if checks_failed == 0:
        if checks_warning == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL SYSTEMS OPERATIONAL{Colors.END}")
            print(f"{Colors.GREEN}System is ready for development and testing!{Colors.END}")
            status = 0
        else:
            print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  SYSTEM MOSTLY WORKING{Colors.END}")
            print(f"{Colors.YELLOW}Some warnings detected, but core functionality is OK{Colors.END}")
            status = 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}🔴 SYSTEM HAS ISSUES{Colors.END}")
        print(f"{Colors.RED}Please fix the {checks_failed} error(s) above{Colors.END}")
        
        if failed_checks:
            print(f"\n{Colors.RED}Failed checks:{Colors.END}")
            for i, check in enumerate(failed_checks, 1):
                print(f"  {i}. {check}")
        
        status = 1
    
    print("="*60)
    
    # Recommendations
    if checks_failed > 0 or checks_warning > 0:
        print(f"\n{Colors.BLUE}📖 Recommendations:{Colors.END}")
        
        if "NOT INSTALLED" in str(failed_checks) and "pip" in str(failed_checks):
            print("  1. Install missing Python packages:")
            print(f"     {Colors.CYAN}pip install -r requirements.txt{Colors.END}")
        
        if any("Flask" in str(check) for check in failed_checks):
            print("  2. Reinstall dependencies:")
            print(f"     {Colors.CYAN}rm -rf venv && python -m venv venv{Colors.END}")
            print(f"     {Colors.CYAN}source venv/bin/activate{Colors.END}")
            print(f"     {Colors.CYAN}pip install -r requirements.txt{Colors.END}")
        
        if any("Docker" in str(check) for check in failed_checks):
            print("  3. Install Docker:")
            print("     Download from https://www.docker.com/products/docker-desktop")
        
        if any("port" in str(check).lower() for check in failed_checks):
            print("  4. Free up port 5000:")
            print(f"     {Colors.CYAN}lsof -ti:5000 | xargs kill -9{Colors.END}")
    
    print(f"\n📚 For detailed diagnostics, see: SYSTEM_DIAGNOSTICS.md")
    print(f"✅ For quick checklist, see: QUICK_DIAGNOSTIC_CHECKLIST.md\n")
    
    return status

if __name__ == "__main__":
    sys.exit(main())
