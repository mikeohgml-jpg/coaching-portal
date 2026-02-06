#!/usr/bin/env python
"""
Quick Start Script for Coaching Portal
Run this script to verify your environment and get started quickly.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check Python version compatibility."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_venv():
    """Check if virtual environment is active."""
    if sys.prefix == sys.base_prefix:
        print("⚠  Virtual environment not active")
        print("   Run: python -m venv venv")
        print("   Then: venv\\Scripts\\activate  (Windows) or source venv/bin/activate (Mac/Linux)")
        return False
    print("✓ Virtual environment active")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    required = [
        'flask',
        'flask_cors',
        'pydantic',
        'google',
        'requests',
        'dotenv'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - not installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists."""
    if Path('.env').exists():
        print("✓ .env file found")
        return True
    else:
        print("⚠  .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then: edit .env with your configuration")
        return False

def check_env_variables():
    """Check if critical environment variables are set."""
    required_vars = [
        'GOOGLE_SHEETS_ID',
        'GOOGLE_CREDENTIALS_JSON',
        'OPENROUTER_API_KEY',
        'FLASK_ENV'
    ]
    
    missing = []
    for var in required_vars:
        if os.getenv(var):
            print(f"✓ {var}")
        else:
            print(f"❌ {var} - not set")
            missing.append(var)
    
    if missing:
        print(f"\n⚠  Missing variables: {', '.join(missing)}")
        return False
    return True

def main():
    """Run all checks."""
    print("=" * 60)
    print("COACHING PORTAL - STARTUP CHECK")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_venv),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Environment Variables", check_env_variables),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * 40)
        result = check_func()
        results.append((check_name, result))
    
    print()
    print("=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    
    all_passed = all(result for _, result in results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    print()
    if all_passed:
        print("✓ All checks passed! You're ready to run:")
        print("  python app.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
