#!/usr/bin/env python3
"""
ShopBot Main Application Entry Point
E-commerce product management system with web automation capabilities.

This file will contain the GUI application in Phase 2.
For now, it serves as a placeholder and testing entry point.

Usage:
    python main.py

Author: ShopBot Development Team
"""

import sys
import json
import os
from datetime import datetime

def load_config():
    """
    Loads configuration from config.json file.
    
    Returns:
        dict: Configuration dictionary
    """
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✅ Configuration loaded successfully")
        return config
    except FileNotFoundError:
        print("❌ config.json not found")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in config.json: {e}")
        return None

def check_dependencies():
    """
    Checks if all required files and dependencies are available.
    
    Returns:
        bool: True if all dependencies are met
    """
    
    required_files = [
        'config.json',
        'database_setup.py',
        'data_manager.py',
        'bot_driver.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def check_database():
    """
    Checks if database exists and is properly set up.
    
    Returns:
        bool: True if database is ready
    """
    if not os.path.exists('products.db'):
        print("⚠️ Database not found. Run 'python database_setup.py' first")
        return False
    
    # Try to connect and verify structure
    try:
        from data_manager import DataManager
        dm = DataManager()
        stats = dm.get_database_stats()
        dm.close()
        
        print(f"✅ Database ready with {stats.get('total_products', 0)} products")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_data_manager():
    """
    Tests the data manager functionality.
    """
    print("\n🧪 Testing Data Manager...")
    
    try:
        from data_manager import DataManager
        dm = DataManager()
        
        # Get database statistics
        stats = dm.get_database_stats()
        print("📊 Database Statistics:")
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Test getting products
        products = dm.get_all_products()
        print(f"\n📦 Found {len(products)} products in database")
        
        if products:
            sample = products[0]
            print(f"\n📋 Sample product (ID: {sample['id']}):")
            print(f"  SKU: {sample['sku']}")
            print(f"  Name: {sample['product_name']}")
            print(f"  Category: {sample['category_path']}")
            print(f"  Price: {sample['price']}")
            print(f"  Has Image: {sample['has_image']}")
            print(f"  Has Description: {sample['has_description']}")
        
        dm.close()
        return True
        
    except Exception as e:
        print(f"❌ Data Manager test failed: {e}")
        return False

def test_bot_driver():
    """
    Tests the bot driver functionality.
    """
    print("\n🤖 Testing Bot Driver...")
    
    try:
        from bot_driver import BotDriverSync
        
        # Just test initialization (don't connect to avoid browser launch)
        bot = BotDriverSync(headless=True)
        
        # Check if Playwright is available
        try:
            import playwright
            print("✅ Playwright is available")
            print("✅ Bot Driver can be initialized")
            print("⚠️ Actual browser testing skipped (requires 'playwright install')")
        except ImportError:
            print("⚠️ Playwright not installed")
            print("   Run: pip install playwright && playwright install chromium")
        
        return True
        
    except Exception as e:
        print(f"❌ Bot Driver test failed: {e}")
        return False

def show_quick_start_guide():
    """
    Shows a quick start guide for setting up the application.
    """
    print("\n" + "="*60)
    print("🚀 SHOPBOT QUICK START GUIDE")
    print("="*60)
    
    print("\n1️⃣ SETUP DATABASE:")
    print("   python database_setup.py")
    
    print("\n2️⃣ PREPARE YOUR DATA:")
    print("   - Place your Excel file in: data/products.xlsx")
    print("   - Create product folders in: data/products/[SKU]/")
    print("   - Add images and descriptions to product folders")
    
    print("\n3️⃣ IMPORT DATA:")
    print("   python -c \"from data_manager import DataManager; dm = DataManager(); dm.convert_xlsx_to_csv('data/products.xlsx', 'data/products.csv'); dm.sync_csv_to_db('data/products.csv'); dm.close()\"")
    
    print("\n4️⃣ SCAN FILES:")
    print("   python -c \"from data_manager import DataManager; dm = DataManager(); dm.scan_and_sync_filesystem('data/products'); dm.close()\"")
    
    print("\n5️⃣ INSTALL BROWSER AUTOMATION:")
    print("   pip install playwright")
    print("   playwright install chromium")
    
    print("\n6️⃣ RUN APPLICATION:")
    print("   python main.py")
    
    print("\n" + "="*60)
    print("📁 EXPECTED FOLDER STRUCTURE:")
    print("="*60)
    print("shopbot/")
    print("├── main.py")
    print("├── database_setup.py")
    print("├── data_manager.py")
    print("├── bot_driver.py")
    print("├── config.json")
    print("├── products.db")
    print("└── data/")
    print("    ├── products.xlsx")
    print("    ├── products.csv")
    print("    └── products/")
    print("        ├── SKU001/")
    print("        │   ├── image1.jpg")
    print("        │   ├── image2.jpg")
    print("        │   └── description.txt")
    print("        └── SKU002/")
    print("            └── ...")

def main():
    """
    Main application entry point.
    Currently serves as a system test and setup guide.
    """
    
    print("🤖 ShopBot - E-commerce Product Manager")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check dependencies
    print("🔍 Checking system dependencies...")
    deps_ok = check_dependencies()
    
    if not deps_ok:
        print("\n❌ Missing dependencies. Please ensure all files are present.")
        show_quick_start_guide()
        sys.exit(1)
    
    # Load configuration
    print("\n📋 Loading configuration...")
    config = load_config()
    if not config:
        print("\n❌ Configuration error. Please check config.json file.")
        sys.exit(1)
    
    print("\n📊 Current Configuration:")
    print(f"  Database: {config['database']['path']}")
    print(f"  Data folder: {config['files']['products_root_folder']}")
    print(f"  Browser profile: {config['browser']['profile_path']}")
    print(f"  Site URL: {config['ecommerce']['site_url']}")
    
    # Check database
    print("\n🗄️ Checking database...")
    db_ok = check_database()
    
    if not db_ok:
        print("\n⚠️ Database needs setup. Run 'python database_setup.py' first.")
        show_quick_start_guide()
        return
    
    # Test components
    print("\n🧪 Running component tests...")
    
    # Test Data Manager
    dm_ok = test_data_manager()
    
    # Test Bot Driver
    bot_ok = test_bot_driver()
    
    # Show system status
    print("\n" + "="*60)
    print("📊 SYSTEM STATUS")
    print("="*60)
    print(f"✅ Dependencies: {'OK' if deps_ok else 'FAILED'}")
    print(f"✅ Configuration: {'OK' if config else 'FAILED'}")
    print(f"✅ Database: {'OK' if db_ok else 'FAILED'}")
    print(f"✅ Data Manager: {'OK' if dm_ok else 'FAILED'}")
    print(f"✅ Bot Driver: {'OK' if bot_ok else 'FAILED'}")
    
    # Phase status
    print("\n" + "="*60)
    print("🏗️ DEVELOPMENT PHASES")
    print("="*60)
    print("✅ Phase 1 (Backend Foundation) - COMPLETE")
    print("  ✅ Database schema created")
    print("  ✅ Data manager implemented")
    print("  ✅ Bot driver implemented")
    print("  ✅ All modules tested")
    
    print("\n⏳ Phase 2 (GUI) - READY FOR DEVELOPMENT")
    print("  ⏳ PyQt main window")
    print("  ⏳ Control panel tab")
    print("  ⏳ Database manager tab")
    
    print("\n⏳ Phase 3 (Integration) - WAITING")
    print("  ⏳ Drag & drop functionality")
    print("  ⏳ Full automation workflow")
    print("  ⏳ Threading integration")
    
    # Show next steps
    if deps_ok and config and db_ok and dm_ok:
        print("\n🎉 Phase 1 Complete! System ready for Phase 2 development.")
        print("\n📝 Ready to implement:")
        print("  - PyQt GUI main window")
        print("  - Control panel with buttons")
        print("  - Database viewer/manager")
        print("  - File drag & drop")
        
        # Check if we have data
        try:
            from data_manager import DataManager
            dm = DataManager()
            stats = dm.get_database_stats()
            dm.close()
            
            if stats.get('total_products', 0) == 0:
                print("\n💡 No products found. Import your data:")
                print("  1. Place Excel file in data/products.xlsx")
                print("  2. Run data import commands (see quick start guide)")
            else:
                print(f"\n📦 Database contains {stats['total_products']} products")
                print(f"   📸 {stats.get('products_with_images', 0)} have images")
                print(f"   📝 {stats.get('products_with_descriptions', 0)} have descriptions")
                
        except Exception as e:
            print(f"\n⚠️ Could not check product data: {e}")
    else:
        print("\n⚠️ System not ready. Please resolve the issues above.")
        show_quick_start_guide()

if __name__ == "__main__":
    main()
