#!/usr/bin/env python3
"""
Database Setup Module for ShopBot
Creates and initializes the SQLite database with the products table schema.

Usage:
    python database_setup.py

This will create a 'products.db' file with the complete product schema.
"""

import sqlite3
import os
from datetime import datetime

def create_database():
    """
    Creates the SQLite database and products table with all required columns.
    
    The schema matches the Hungarian spreadsheet structure with additional
    tracking fields for file management and upload status.
    """
    
    # Database file path
    db_path = "products.db"
    
    # Remove existing database if it exists (for clean setup)
    if os.path.exists(db_path):
        print(f"Removing existing database: {db_path}")
        os.remove(db_path)
    
    # Create new database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create products table with complete schema
    create_table_sql = """
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT UNIQUE NOT NULL,
        product_name TEXT NOT NULL,
        category_path TEXT,
        size_cm TEXT,
        parts_count INTEGER,
        color TEXT,
        material TEXT,
        thickness TEXT,
        price NUMERIC,
        main_image_filename TEXT,
        extra_image_filenames TEXT,  -- JSON list of additional images
        description_filename TEXT,
        has_image BOOLEAN DEFAULT 0,
        has_description BOOLEAN DEFAULT 0,
        is_uploaded BOOLEAN DEFAULT 0,
        is_active BOOLEAN DEFAULT 1,
        last_checked_timestamp TEXT,
        last_modified_timestamp TEXT,
        created_timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    try:
        cursor.execute(create_table_sql)
        
        # Create indexes for better performance
        cursor.execute("CREATE INDEX idx_sku ON products(sku)")
        cursor.execute("CREATE INDEX idx_category ON products(category_path)")
        cursor.execute("CREATE INDEX idx_active ON products(is_active)")
        cursor.execute("CREATE INDEX idx_uploaded ON products(is_uploaded)")
        
        conn.commit()
        print(f"✅ Database created successfully: {db_path}")
        print("✅ Products table created with all required columns")
        print("✅ Indexes created for better performance")
        
        # Display table schema for verification
        cursor.execute("PRAGMA table_info(products)")
        columns = cursor.fetchall()
        
        print("\n📋 Table Schema:")
        for col in columns:
            nullable = "" if col[3] else "NULL"
            default = f"DEFAULT {col[4]}" if col[4] else ""
            print(f"  {col[1]} ({col[2]}) {nullable} {default}".strip())
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        
    finally:
        conn.close()

def verify_database():
    """
    Verifies that the database was created correctly.
    """
    
    db_path = "products.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if products table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            # Count expected columns
            cursor.execute("PRAGMA table_info(products)")
            columns = cursor.fetchall()
            expected_columns = 19  # Total columns we expect
            
            if len(columns) >= expected_columns:
                print("✅ Database verification successful")
                print(f"✅ Found {len(columns)} columns in products table")
                return True
            else:
                print(f"❌ Expected {expected_columns} columns, found {len(columns)}")
                return False
        else:
            print("❌ Products table not found")
            return False
            
    except sqlite3.Error as e:
        print(f"❌ Database verification error: {e}")
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Setting up ShopBot database...")
    print("=" * 50)
    create_database()
    print("\n🔍 Verifying database setup...")
    if verify_database():
        print("\n🎉 Database setup complete!")
        print("\nNext steps:")
        print("1. Run: python data_manager.py (to test data operations)")
        print("2. Run: python main.py (to start the application)")
    else:
        print("\n❌ Database setup failed!")
