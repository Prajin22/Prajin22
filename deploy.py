#!/usr/bin/env python3
"""
Deployment Helper Script
This script helps prepare your Flask app for deployment.
"""

import os
import secrets
import string
from pathlib import Path

def generate_secret_key(length=32):
    """Generate a random secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_fernet_key():
    """Generate a proper Fernet key"""
    from cryptography.fernet import Fernet
    return Fernet.generate_key().decode()

def create_env_file():
    """Create a .env file with proper environment variables"""
    
    # Generate proper keys
    secret_key = generate_secret_key(32)
    fernet_key = generate_fernet_key()
    
    env_content = f"""# Production Environment Variables
# DO NOT COMMIT THIS FILE TO GIT!

# Flask Configuration
SECRET_KEY={secret_key}
FLASK_ENV=production
FLASK_DEBUG=False

# Database Configuration
DATABASE_URL=sqlite:///jobportal.db

# Encryption
ENCRYPTION_KEY={fernet_key}

# Security
WTF_CSRF_ENABLED=True
"""
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with production environment variables")
    print("⚠️  IMPORTANT: Add .env to your .gitignore file!")
    return secret_key, fernet_key

def check_deployment_readiness():
    """Check if your app is ready for deployment"""
    
    print("🔍 Checking deployment readiness...")
    
    # Check required files
    required_files = [
        'main.py',
        'requirements.txt',
        'render.yaml',
        'Procfile',
        'runtime.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    # Check if database is ready
    if not Path('instance/jobportal.db').exists():
        print("❌ Database file not found. Run the app first to create it.")
        return False
    
    print("✅ All required files present")
    print("✅ Database file exists")
    print("✅ App is ready for deployment!")
    return True

def main():
    """Main deployment helper function"""
    
    print("🚀 LinkedIn Job Portal - Deployment Helper")
    print("=" * 50)
    
    # Check readiness
    if not check_deployment_readiness():
        print("\n❌ Please fix the issues above before deploying.")
        return
    
    # Create environment file
    print("\n🔧 Setting up environment variables...")
    secret_key, fernet_key = create_env_file()
    
    print("\n📋 Next Steps for Deployment:")
    print("1. Push your code to GitHub:")
    print("   git add .")
    print("   git commit -m 'Prepare for deployment'")
    print("   git push origin main")
    
    print("\n2. Deploy to Render (Recommended):")
    print("   - Go to render.com and sign up/login")
    print("   - Click 'New +' → 'Web Service'")
    print("   - Connect your GitHub repository")
    print("   - Set environment variables:")
    print(f"     ENCRYPTION_KEY: {fernet_key}")
    print(f"     SECRET_KEY: {secret_key}")
    print("   - Click 'Create Web Service'")
    
    print("\n3. Or deploy to Railway:")
    print("   npm install -g @railway/cli")
    print("   railway login")
    print("   railway init")
    print("   railway up")
    
    print("\n4. Or deploy to Heroku:")
    print("   heroku login")
    print("   heroku create your-app-name")
    print("   git push heroku main")
    
    print("\n🎉 Your app will be live at the provided URL!")
    
    # Save keys for easy copy-paste
    with open('deployment_keys.txt', 'w') as f:
        f.write(f"ENCRYPTION_KEY={fernet_key}\n")
        f.write(f"SECRET_KEY={secret_key}\n")
    
    print(f"\n💾 Keys saved to 'deployment_keys.txt' for easy reference")

if __name__ == "__main__":
    main()
