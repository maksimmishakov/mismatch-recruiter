#!/usr/bin/env python3
"""
MisMatch Recruiter - System Diagnostic Check
Automatically verifies all components and dependencies
"""

import sys
import os
import subprocess
import json
from datetime import datetime

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'
BOLD = '\033[1m'

class SystemCheck:
    def __init__(self):
        self.checks = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.timestamp = datetime.now().isoformat()

    def print_header(self):
        print(f"\n{BLUE}{BOLD}═══════════════════════════════════════════════════════════════{END}")
        print(f"{BLUE}{BOLD}MisMatch Recruiter - System Diagnostic Check{END}")
        print(f"{BLUE}{BOLD}═══════════════════════════════════════════════════════════════{END}\n")
        print(f"Timestamp: {self.timestamp}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Platform: {sys.platform}\n")

    def check(self, name, condition, details=""):
        """
        Log a check result
        """
        if condition is True:
            status = f"{GREEN}✓ PASS{END}"
            self.passed += 1
        elif condition is False:
            status = f"{RED}✗ FAIL{END}"
            self.failed += 1
        else:  # Warning
            status = f"{YELLOW}⚠ WARN{END}"
            self.warnings += 1
        
        output = f"{status} {name}"
        if details:
            output += f" [{details}]"
        print(output)
        self.checks.append((name, condition, details))

    def run_command(self, cmd, capture=False):
        """
        Run shell command and return output
        """
        try:
            if capture:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
                return result.stdout.strip(), result.returncode == 0
            else:
                return subprocess.run(cmd, shell=True, timeout=5).returncode == 0
        except Exception as e:
            return str(e), False

    def check_python(self):
        print(f"{BOLD}\n1. Python Environment{END}")
        print("─" * 40)
        
        # Python version
        version = sys.version.split()[0]
        major, minor = map(int, version.split('.')[:2])
        self.check(f"Python Version", (major, minor) >= (3, 9), f"{version}")
        
        # Virtual environment
        venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        self.check("Virtual Environment", venv_active or 'VIRTUAL_ENV' in os.environ, 
                  os.environ.get('VIRTUAL_ENV', 'Not detected'))

    def check_dependencies(self):
        print(f"{BOLD}\n2. Python Dependencies{END}")
        print("─" * 40)
        
        packages = {
            'flask': 'Flask',
            'flask_cors': 'Flask-CORS',
            'sqlalchemy': 'SQLAlchemy',
            'psycopg2': 'psycopg2-binary',
            'redis': 'redis',
            'requests': 'requests',
        }
        
        for import_name, display_name in packages.items():
            try:
                mod = __import__(import_name)
                version = getattr(mod, '__version__', 'unknown')
                self.check(display_name, True, f"v{version}")
            except ImportError:
                self.check(display_name, False, "Not installed")

    def check_files(self):
        print(f"{BOLD}\n3. Project Files{END}")
        print("─" * 40)
        
        files = {
            'app.py': 'Main Flask application',
            'requirements.txt': 'Python dependencies',
            'docker-compose.yml': 'Docker Compose config',
            '.env': 'Environment variables',
            '.devcontainer/devcontainer.json': 'Codespaces config',
        }
        
        for filepath, description in files.items():
            exists = os.path.exists(filepath)
            if exists:
                size = os.path.getsize(filepath)
                self.check(description, exists, f"{filepath} ({size} bytes)")
            else:
                self.check(description, False, f"{filepath} NOT FOUND")

    def check_ports(self):
        print(f"{BOLD}\n4. Network & Ports{END}")
        print("─" * 40)
        
        ports = {
            5000: 'Backend API',
            5432: 'PostgreSQL',
            6379: 'Redis',
            3000: 'Frontend',
            9090: 'Prometheus',
            3001: 'Grafana',
        }
        
        for port, service in ports.items():
            # Try to check if port is available
            cmd = f"lsof -i :{port}" if sys.platform != 'win32' else f"netstat -ano | findstr :{port}"
            available = not self.run_command(cmd)
            status = "Available" if available else "In use"
            self.check(f"Port {port} ({service})", available, status)

    def check_docker(self):
        print(f"{BOLD}\n5. Docker{END}")
        print("─" * 40)
        
        # Docker installed
        docker_installed, _ = self.run_command("docker --version", capture=True)
        self.check("Docker installed", bool(docker_installed), docker_installed.strip())
        
        # Docker daemon running
        docker_running, _ = self.run_command("docker ps", capture=True)
        self.check("Docker daemon", bool(docker_running != ""), "Running" if docker_running else "Not running")
        
        # Docker Compose installed
        compose_installed, _ = self.run_command("docker-compose --version", capture=True)
        self.check("Docker Compose", bool(compose_installed), compose_installed.strip() if compose_installed else "Not found")

    def check_git(self):
        print(f"{BOLD}\n6. Git Repository{END}")
        print("─" * 40)
        
        # Git installed
        git_installed, _ = self.run_command("git --version", capture=True)
        self.check("Git installed", bool(git_installed), git_installed.strip())
        
        # Git repository initialized
        git_repo, _ = self.run_command("git rev-parse --git-dir", capture=True)
        self.check("Git repository", bool(git_repo), git_repo if git_repo else "Not a git repo")
        
        # Check commits
        commits, _ = self.run_command("git rev-list --all --count", capture=True)
        if commits:
            self.check(f"Commits", True, commits.strip())

    def check_api(self):
        print(f"{BOLD}\n7. API Endpoints{END}")
        print("─" * 40)
        
        try:
            import requests
            endpoints = {
                'health': '/health',
                'candidates': '/api/v1/candidates',
                'jobs': '/api/v1/jobs',
                'matches': '/api/v1/matches',
            }
            
            for name, endpoint in endpoints.items():
                try:
                    response = requests.get(f'http://localhost:5000{endpoint}', timeout=2)
                    self.check(f"API {name}", response.status_code < 500, f"Status {response.status_code}")
                except requests.exceptions.ConnectionError:
                    self.check(f"API {name}", None, "Backend not running")
                except Exception as e:
                    self.check(f"API {name}", None, str(e)[:30])
        except ImportError:
            self.check("requests library", False, "Not installed")

    def check_security(self):
        print(f"{BOLD}\n8. Security{END}")
        print("─" * 40)
        
        # Check for secrets in code
        found_secrets = False
        try:
            result = subprocess.run(
                "grep -r 'password\\|api_key\\|secret' app.py",
                shell=True,
                capture_output=True,
                timeout=5
            )
            found_secrets = result.returncode == 0
        except:
            pass
        
        self.check("No hardcoded secrets", not found_secrets)
        
        # Check .env not in git
        env_in_git = False
        try:
            result = subprocess.run(
                "git ls-files | grep .env",
                shell=True,
                capture_output=True,
                timeout=5
            )
            env_in_git = result.returncode == 0
        except:
            pass
        
        self.check(".env not committed", not env_in_git)
        
        # Check debug mode
        debug_enabled = False
        try:
            with open('app.py', 'r') as f:
                debug_enabled = 'debug=True' in f.read()
        except:
            pass
        
        self.check("Debug mode disabled", not debug_enabled)

    def print_summary(self):
        print(f"\n{BLUE}{BOLD}═══════════════════════════════════════════════════════════════{END}")
        print(f"{GREEN}✓ Passed: {self.passed}{END}")
        print(f"{YELLOW}⚠ Warnings: {self.warnings}{END}")
        print(f"{RED}✗ Failed: {self.failed}{END}")
        print(f"{BLUE}{BOLD}═══════════════════════════════════════════════════════════════{END}")
        
        total = self.passed + self.warnings + self.failed
        if self.failed == 0:
            print(f"\n{GREEN}{BOLD}🎉 ALL SYSTEMS OPERATIONAL{END}\n")
            if self.warnings > 0:
                print(f"{YELLOW}⚠️  Note: {self.warnings} warnings - review recommended{END}\n")
            return 0
        else:
            print(f"\n{RED}{BOLD}❌ SYSTEM CHECK FAILED{END}")
            print(f"{RED}Please fix {self.failed} issues and try again{END}\n")
            return 1

    def run(self):
        self.print_header()
        
        try:
            self.check_python()
            self.check_dependencies()
            self.check_files()
            self.check_ports()
            self.check_docker()
            self.check_git()
            self.check_api()
            self.check_security()
        except Exception as e:
            print(f"{RED}Error during checks: {e}{END}")
            return 1
        
        return self.print_summary()

if __name__ == '__main__':
    checker = SystemCheck()
    sys.exit(checker.run())
