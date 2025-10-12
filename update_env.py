#!/usr/bin/env python3
"""
Update .env file with missing variables
"""

import os

def update_env_file():
    """Add missing environment variables to .env file"""
    
    # Read existing .env file
    env_file = '.env'
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        return False
    
    # Read current content
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Check what's missing
    missing_vars = []
    
    required_vars = {
        'FRONTEND_URL': 'http://localhost:3000',
        'ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_MINUTES': '30',
        'CORS_ORIGINS': 'http://localhost:3000,http://127.0.0.1:3000,http://niktick.ir'
    }
    
    for var, default_value in required_vars.items():
        if f'{var}=' not in content:
            missing_vars.append(f'{var}={default_value}')
    
    if not missing_vars:
        print("✅ All required environment variables are already present!")
        return True
    
    # Add missing variables
    print("🔧 Adding missing environment variables...")
    with open(env_file, 'a') as f:
        f.write('\n# Additional variables for invitation system\n')
        for var in missing_vars:
            f.write(f'{var}\n')
            print(f"   ✅ Added: {var}")
    
    print(f"\n🎉 Successfully added {len(missing_vars)} missing variables!")
    return True

if __name__ == "__main__":
    update_env_file()
