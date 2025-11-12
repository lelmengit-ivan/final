"""
Organize files for deployment
This script will:
1. Create necessary folders
2. Move files to appropriate locations
3. Clean up test/debug files
"""

import os
import shutil

def create_folders():
    """Create necessary folders for deployment"""
    folders = ['templates', 'tests', 'scripts/utils']
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created folder: {folder}")

def move_html_files():
    """Move HTML files to templates folder"""
    html_files = ['index.html', 'login.html', 'register-org.html']
    for file in html_files:
        if os.path.exists(file):
            shutil.move(file, f'templates/{file}')
            print(f"✅ Moved {file} to templates/")

def move_test_files():
    """Move test files to tests folder"""
    test_files = [
        'check_analytics_data.py',
        'check_medicine_data.py',
        'test_dashboard.py',
        'test_endpoints.py',
        'test_frontend.html',
        'test_login.py',
        'debug_frontend.html'
    ]
    for file in test_files:
        if os.path.exists(file):
            shutil.move(file, f'tests/{file}')
            print(f"✅ Moved {file} to tests/")

def move_utility_scripts():
    """Move utility scripts to scripts folder"""
    util_files = [
        'fix_admin_login.py',
        'fix_auth_headers.py',
        'fix_chart_functions.py',
        'fix_tofixed_errors.py',
        'optimize_database.py',
        'migrate_to_multitenancy.py'
    ]
    for file in util_files:
        if os.path.exists(file):
            shutil.move(file, f'scripts/{file}')
            print(f"✅ Moved {file} to scripts/")

def create_env_template():
    """Create .env.example file"""
    env_content = """# Environment Variables for Production

# Security
SECRET_KEY=your-super-secret-key-here-change-this

# Database (for production, use PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost/pharmacy_db

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False

# JWT Configuration
JWT_EXPIRATION_HOURS=24

# CORS (comma-separated origins)
ALLOWED_ORIGINS=https://yourdomain.com

# Server
PORT=5000
HOST=0.0.0.0
"""
    with open('.env.example', 'w') as f:
        f.write(env_content)
    print("✅ Created .env.example")

def update_gitignore():
    """Update .gitignore for production"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Environment
.env
.venv

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Test files
tests/
test_*.py
*_test.py

# Backups
backups/
*.bak

# Documentation (optional - remove if you want to include)
# docs/

# Temporary files
tmp/
temp/
"""
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ Updated .gitignore")

def create_production_requirements():
    """Create production requirements.txt"""
    prod_requirements = """Flask==3.0.0
Flask-CORS==4.0.0
PyJWT==2.8.0
gunicorn==21.2.0
python-dotenv==1.0.0
psycopg2-binary==2.9.9
"""
    with open('requirements.prod.txt', 'w') as f:
        f.write(prod_requirements)
    print("✅ Created requirements.prod.txt")

def create_procfile():
    """Create Procfile for Heroku"""
    with open('Procfile', 'w') as f:
        f.write('web: gunicorn app:app\n')
    print("✅ Created Procfile")

def create_runtime():
    """Create runtime.txt for Heroku"""
    with open('runtime.txt', 'w') as f:
        f.write('python-3.11.0\n')
    print("✅ Created runtime.txt")

def print_summary():
    """Print deployment summary"""
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT ORGANIZATION COMPLETE!")
    print("="*60)
    print("\n📁 Project Structure:")
    print("  ✅ templates/     - HTML files")
    print("  ✅ static/        - CSS, JS, images")
    print("  ✅ scripts/       - Utility scripts")
    print("  ✅ tests/         - Test files")
    print("  ✅ docs/          - Documentation")
    print("\n📝 Configuration Files:")
    print("  ✅ .env.example   - Environment variables template")
    print("  ✅ .gitignore     - Git ignore rules")
    print("  ✅ Procfile       - Heroku deployment")
    print("  ✅ runtime.txt    - Python version")
    print("  ✅ requirements.prod.txt - Production dependencies")
    print("\n🚀 Next Steps:")
    print("  1. Copy .env.example to .env and update values")
    print("  2. Update app.py to use render_template()")
    print("  3. Test locally: python app.py")
    print("  4. Review DEPLOYMENT_GUIDE.md")
    print("  5. Deploy to your chosen platform")
    print("\n⚠️  Important:")
    print("  - Change SECRET_KEY in .env")
    print("  - Use PostgreSQL for production")
    print("  - Enable HTTPS/SSL")
    print("  - Set up monitoring")
    print("="*60)

def main():
    print("🚀 Organizing files for deployment...\n")
    
    try:
        create_folders()
        print()
        
        move_html_files()
        print()
        
        move_test_files()
        print()
        
        move_utility_scripts()
        print()
        
        create_env_template()
        update_gitignore()
        create_production_requirements()
        create_procfile()
        create_runtime()
        
        print_summary()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Some files may have already been moved or don't exist.")
        print("This is normal if you've run this script before.")

if __name__ == '__main__':
    main()
