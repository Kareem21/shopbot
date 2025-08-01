#!/usr/bin/env python3
"""
ShopBot Setup Script
Automates the initial setup of the ShopBot application.

Usage:
    python setup.py

This script will:
1. Create necessary directories
2. Set up the database
3. Install dependencies (if requested)
4. Create sample data structure
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def create_directories():
    """
    Creates the necessary directory structure.
    """
    print("📁 Creating directory structure...")
    
    directories = [
        'data',
        'data/products',
        'chrome_profile',
        'logs',
        'backups'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ Created: {directory}")
    
    print("✅ Directory structure created")

def setup_database():
    """
    Sets up the database using database_setup.py
    """
    print("\n🗄️ Setting up database...")
    
    try:
        # Import and run database setup
        import database_setup
        print("✅ Database setup completed")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def create_sample_config():
    """
    Creates a sample configuration file if it doesn't exist.
    """
    if os.path.exists('config.json'):
        print("✅ config.json already exists")
        return
    
    print("\n⚙️ Creating sample config.json...")
    
    sample_config = {
        "database": {
            "path": "products.db",
            "backup_enabled": True,
            "backup_interval_hours": 24
        },
        "files": {
            "product_data_xlsx": "data/products.xlsx",
            "product_data_csv": "data/products_sanitized.csv",
            "products_root_folder": "data/products",
            "images_folder": "data/products/images",
            "descriptions_folder": "data/products/descriptions"
        },
        "browser": {
            "profile_path": "chrome_profile",
            "headless": False,
            "timeout_seconds": 30,
            "retry_attempts": 3
        },
        "ecommerce": {
            "site_url": "https://your-shop.com",
            "login_url": "https://your-shop.com/admin/login",
            "upload_url": "https://your-shop.com/admin/products/upload"
        },
        "logging": {
            "level": "INFO",
            "file": "logs/shopbot.log",
            "max_size_mb": 10,
            "backup_count": 5
        },
        "sync": {
            "check_interval_minutes": 60,
            "batch_size": 10,
            "concurrent_uploads": 2
        }
    }
    
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(sample_config, f, indent=2, ensure_ascii=False)
    
    print("✅ config.json created")

def install_dependencies():
    """
    Installs Python dependencies.
    """
    print("\n📦 Installing dependencies...")
    
    # Ask user if they want to install dependencies
    response = input("Install Python dependencies? (y/N): ").lower().strip()
    
    if response in ['y', 'yes']:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("✅ Dependencies installed successfully")
            
            # Install Playwright browsers
            response = input("Install Playwright browsers? (y/N): ").lower().strip()
            if response in ['y', 'yes']:
                subprocess.check_call([sys.executable, '-m', 'playwright', 'install', 'chromium'])
                print("✅ Playwright browsers installed")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Dependency installation failed: {e}")
            return False
    else:
        print("⏭️ Skipping dependency installation")
        return True

def create_sample_data():
    """
    Creates sample data structure and files.
    """
    print("\n📊 Creating sample data structure...")
    
    # Create sample product folders
    sample_skus = ['SKU001', 'SKU002', 'SKU003']
    
    for sku in sample_skus:
        product_dir = f'data/products/{sku}'
        os.makedirs(product_dir, exist_ok=True)
        
        # Create sample description file
        desc_file = os.path.join(product_dir, 'description.txt')
        with open(desc_file, 'w', encoding='utf-8') as f:
            f.write(f"Sample product description for {sku}\n")
            f.write("This is a placeholder description file.\n")
            f.write("Replace with actual product descriptions.")
        
        print(f"  ✅ Created sample folder: {product_dir}")
    
    # Create sample Excel file structure info
    sample_excel_info = """
📋 EXCEL FILE FORMAT EXPECTED:

Your Excel file should have these columns (Hungarian names):
- Kategória: Main category
- Kategória 2: Subcategory  
- Kategória 3: Sub-subcategory
- Termék kód: Product SKU/Code
- Terméknév: Product name
- Méret (cm): Size in cm
- Részek száma: Number of parts
- Szín: Color
- Anyag: Material
- Vastagság: Thickness
- Ár: Price (format: "13.990 ; 8990")

Place your Excel file at: data/products.xlsx
"""
    
    with open('data/EXCEL_FORMAT.txt', 'w', encoding='utf-8') as f:
        f.write(sample_excel_info)
    
    print("✅ Sample data structure created")
    print("📝 Excel format guide created: data/EXCEL_FORMAT.txt")

def verify_setup():
    """
    Verifies that the setup was completed correctly.
    """
    print("\n🔍 Verifying setup...")
    
    required_files = [
        'config.json',
        'database_setup.py',
        'data_manager.py',
        'bot_driver.py',
        'main.py',
        'products.db'
    ]
    
    required_dirs = [
        'data',
        'data/products',
        'chrome_profile'
    ]
    
    # Check files
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"  ✅ {file}")
    
    # Check directories
    missing_dirs = []
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
        else:
            print(f"  ✅ {directory}/")
    
    if missing_files or missing_dirs:
        print(f"\n❌ Setup incomplete:")
        if missing_files:
            print(f"  Missing files: {', '.join(missing_files)}")
        if missing_dirs:
            print(f"  Missing directories: {', '.join(missing_dirs)}")
        return False
    else:
        print("\n✅ Setup verification successful!")
        return True

def show_next_steps():
    """
    Shows the next steps after setup completion.
    """
    print("\n" + "="*60)
    print("🎉 SHOPBOT SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 NEXT STEPS:")
    print("1️⃣ Place your Excel file at: data/products.xlsx")
    print("2️⃣ Add product images to: data/products/[SKU]/")
    print("3️⃣ Add product descriptions to: data/products/[SKU]/")
    print("4️⃣ Import your data:")
    print("   python -c \"from data_manager import DataManager; dm = DataManager(); dm.convert_xlsx_to_csv('data/products.xlsx', 'data/products.csv'); dm.sync_csv_to_db('data/products.csv'); dm.scan_and_sync_filesystem('data/products'); dm.close()\"")
    print("5️⃣ Test the system:")
    print("   python main.py")
    
    print("\n🔧 CONFIGURATION:")
    print("- Edit config.json to customize settings")
    print("- Update e-commerce site URLs in config.json")
    print("- Modify bot_driver.py for your specific site")
    
    print("\n📁 FOLDER STRUCTURE:")
    print("shopbot/")
    print("├── main.py              # Main application")
    print("├── database_setup.py    # Database initialization")
    print("├── data_manager.py      # Data operations")
    print("├── bot_driver.py        # Web automation")
    print("├── config.json          # Configuration")
    print("├── requirements.txt     # Dependencies")
    print("├── products.db          # SQLite database")
    print("└── data/")
    print("    ├── products.xlsx    # Your Excel file (place here)")
    print("    └── products/        # Product folders")
    print("        ├── SKU001/")
    print("        │   ├── image1.jpg")
    print("        │   └── description.txt")
    print("        └── SKU002/")
    print("            └── ...")

def main():
    """
    Main setup function.
    """
    print("🚀 ShopBot Setup Script")
    print("=" * 50)
    print("This script will set up your ShopBot environment.\n")
    
    # Create directories
    create_directories()
    
    # Create sample config
    create_sample_config()
    
    # Setup database
    db_ok = setup_database()
    
    # Install dependencies
    deps_ok = install_dependencies()
    
    # Create sample data structure
    create_sample_data()
    
    # Verify setup
    setup_ok = verify_setup()
    
    # Show results
    print("\n" + "="*60)
    print("📊 SETUP SUMMARY")
    print("="*60)
    print(f"✅ Directories: Created")
    print(f"✅ Configuration: Created")
    print(f"{'✅' if db_ok else '❌'} Database: {'Ready' if db_ok else 'Failed'}")
    print(f"{'✅' if deps_ok else '⚠️'} Dependencies: {'Installed' if deps_ok else 'Skipped'}")
    print(f"✅ Sample Data: Created")
    print(f"{'✅' if setup_ok else '❌'} Verification: {'Passed' if setup_ok else 'Failed'}")
    
    if setup_ok:
        show_next_steps()
    else:
        print("\n❌ Setup incomplete. Please resolve the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()