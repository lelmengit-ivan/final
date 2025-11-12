"""
Quick setup script for Vercel deployment
"""
import os
import shutil

def setup_for_vercel():
    print("🚀 Setting up for Vercel deployment...\n")
    
    # 1. Create templates folder
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("✅ Created templates/ folder")
    
    # 2. Move HTML files
    html_files = ['index.html', 'login.html', 'register-org.html']
    for file in html_files:
        if os.path.exists(file):
            shutil.copy(file, f'templates/{file}')
            print(f"✅ Copied {file} to templates/")
    
    # 3. Create .env.example
    env_content = """# Vercel Environment Variables
SECRET_KEY=your-secret-key-here
POSTGRES_URL=postgresql://user:pass@host:5432/dbname
JWT_EXPIRATION_HOURS=24
ALLOWED_ORIGINS=https://yourdomain.vercel.app
"""
    with open('.env.vercel.example', 'w') as f:
        f.write(env_content)
    print("✅ Created .env.vercel.example")
    
    print("\n" + "="*60)
    print("✅ VERCEL SETUP COMPLETE!")
    print("="*60)
    print("\n📝 Next Steps:")
    print("  1. Install Vercel CLI: npm install -g vercel")
    print("  2. Login: vercel login")
    print("  3. Update app.py (see VERCEL_DEPLOYMENT.md)")
    print("  4. Set up database (PostgreSQL recommended)")
    print("  5. Deploy: vercel --prod")
    print("\n📖 Full Guide: VERCEL_DEPLOYMENT.md")
    print("="*60 + "\n")

if __name__ == '__main__':
    setup_for_vercel()
