#!/usr/bin/env python3
"""
Data Manager Module for ShopBot
Handles all database operations and file system synchronization.

This module manages:
- Excel/CSV data import and sanitization
- SQLite database operations
- File system scanning for images and descriptions
- Product data CRUD operations

Usage:
    from data_manager import DataManager
    dm = DataManager("products.db")
    dm.sync_csv_to_db("data/products.csv")
"""

import sqlite3
import pandas as pd
import json
import os
import glob
import re
from datetime import datetime
from pathlib import Path

class DataManager:
    """
    Manages all data operations for the ShopBot application.
    
    Handles database connections, data import/export, and file system operations.
    """
    
    def __init__(self, db_path="products.db"):
        """
        Initialize the DataManager with database connection.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self._connect_to_database()
    
    def _connect_to_database(self):
        """
        Establishes connection to the SQLite database.
        Creates the database if it doesn't exist.
        """
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            print(f"✅ Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"❌ Database connection error: {e}")
            raise
    
    def convert_xlsx_to_csv(self, xlsx_path, csv_path):
        """
        Converts Excel file to sanitized CSV format.
        
        Handles Hungarian characters and cleans data for database import.
        
        Args:
            xlsx_path (str): Path to the input Excel file
            csv_path (str): Path for the output CSV file
            
        Returns:
            bool: True if conversion successful
        """
        try:
            print(f"📊 Converting {xlsx_path} to {csv_path}")
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            
            # Read Excel file with proper encoding
            df = pd.read_excel(xlsx_path, engine='openpyxl')
            
            # Clean column names (remove extra spaces)
            df.columns = df.columns.str.strip()
            
            # Remove completely empty rows
            df = df.dropna(how='all')
            
            # Save as CSV with UTF-8 encoding
            df.to_csv(csv_path, index=False, encoding='utf-8')
            
            print(f"✅ Converted {len(df)} rows to CSV")
            print(f"✅ Columns found: {list(df.columns)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Excel conversion error: {e}")
            return False
    
    def _build_category_path(self, row):
        """
        Builds category path from Kategória columns.
        
        Args:
            row: Pandas row with category data
            
        Returns:
            str: Category path like "Természet/Virágok"
        """
        categories = []
        
        # Check each category column
        for col in ['Kategória', 'Kategória 2', 'Kategória 3']:
            if col in row and pd.notna(row[col]) and str(row[col]).strip():
                categories.append(str(row[col]).strip())
        
        return '/'.join(categories) if categories else ''
    
    def _parse_price(self, price_str):
        """
        Parses price from format "13.990 ; 8990" to extract main price.
        
        Args:
            price_str: Price string from spreadsheet
            
        Returns:
            float: Parsed price or 0.0 if parsing fails
        """
        if pd.isna(price_str) or not str(price_str).strip():
            return 0.0
            
        try:
            # Convert to string and clean
            price_clean = str(price_str).strip()
            
            # Handle format "13.990 ; 8990" - take first price
            if ';' in price_clean:
                price_clean = price_clean.split(';')[0].strip()
            
            # Remove spaces and convert to float
            price_clean = price_clean.replace(' ', '').replace('.', '')
            
            return float(price_clean)
            
        except (ValueError, AttributeError):
            print(f"⚠️ Could not parse price: {price_str}")
            return 0.0
    
    def _parse_parts_count(self, parts_str):
        """
        Parses parts count from "Részek száma" column.
        
        Args:
            parts_str: Parts count string
            
        Returns:
            int: Parts count or 0 if parsing fails
        """
        if pd.isna(parts_str):
            return 0
            
        try:
            return int(str(parts_str).strip())
        except (ValueError, AttributeError):
            return 0
    
    def sync_csv_to_db(self, csv_path):
        """
        Syncs CSV data to the database.
        
        Reads the sanitized CSV and updates the SQLite database with proper
        mapping of Hungarian columns to database fields.
        
        Args:
            csv_path (str): Path to the CSV file
            
        Returns:
            int: Number of products processed
        """
        if not os.path.exists(csv_path):
            print(f"❌ CSV file not found: {csv_path}")
            return 0
        
        try:
            print(f"📥 Reading CSV: {csv_path}")
            df = pd.read_csv(csv_path, encoding='utf-8')
            
            print(f"📊 Processing {len(df)} rows from CSV")
            print(f"📋 Columns: {list(df.columns)}")
            
            cursor = self.connection.cursor()
            processed = 0
            errors = 0
            
            for index, row in df.iterrows():
                try:
                    # Skip rows without product code
                    if pd.isna(row.get('Termék kód', '')) or not str(row['Termék kód']).strip():
                        continue
                    
                    # Map Hungarian columns to database fields
                    product_data = {
                        'sku': str(row['Termék kód']).strip(),
                        'product_name': str(row.get('Terméknév', '')).strip(),
                        'category_path': self._build_category_path(row),
                        'size_cm': str(row.get('Méret (cm)', '')).strip(),
                        'parts_count': self._parse_parts_count(row.get('Részek száma')),
                        'color': str(row.get('Szín', '')).strip(),
                        'material': str(row.get('Anyag', '')).strip(),
                        'thickness': str(row.get('Vastagság', '')).strip(),
                        'price': self._parse_price(row.get('Ár')),
                        'last_modified_timestamp': datetime.now().isoformat()
                    }
                    
                    # Insert or update product
                    insert_sql = """
                    INSERT OR REPLACE INTO products 
                    (sku, product_name, category_path, size_cm, parts_count, color, 
                     material, thickness, price, last_modified_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    
                    cursor.execute(insert_sql, (
                        product_data['sku'],
                        product_data['product_name'],
                        product_data['category_path'],
                        product_data['size_cm'],
                        product_data['parts_count'],
                        product_data['color'],
                        product_data['material'],
                        product_data['thickness'],
                        product_data['price'],
                        product_data['last_modified_timestamp']
                    ))
                    
                    processed += 1
                    
                except Exception as e:
                    errors += 1
                    print(f"⚠️ Error processing row {index}: {e}")
                    continue
            
            self.connection.commit()
            
            print(f"✅ Processed {processed} products successfully")
            if errors > 0:
                print(f"⚠️ {errors} rows had errors")
            
            return processed
            
        except Exception as e:
            print(f"❌ CSV sync error: {e}")
            return 0
    
    def scan_and_sync_filesystem(self, root_folder_path):
        """
        Scans the file system for product images and descriptions.
        
        Updates database flags (has_image, has_description) based on
        files found in the product folders.
        
        Args:
            root_folder_path (str): Root folder containing product subfolders
            
        Returns:
            dict: Statistics about files found
        """
        if not os.path.exists(root_folder_path):
            print(f"❌ Root folder not found: {root_folder_path}")
            return {'images': 0, 'descriptions': 0, 'updated': 0}
        
        print(f"🔍 Scanning filesystem: {root_folder_path}")
        
        stats = {'images': 0, 'descriptions': 0, 'updated': 0}
        cursor = self.connection.cursor()
        
        # Get all products from database
        cursor.execute("SELECT id, sku FROM products")
        products = cursor.fetchall()
        
        for product in products:
            product_id = product['id']
            sku = product['sku']
            
            # Look for product folder (by SKU)
            product_folder = os.path.join(root_folder_path, sku)
            
            has_image = False
            has_description = False
            main_image = None
            extra_images = []
            description_file = None
            
            if os.path.exists(product_folder):
                # Scan for image files
                image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']
                image_files = []
                
                for ext in image_extensions:
                    image_files.extend(glob.glob(os.path.join(product_folder, ext)))
                
                if image_files:
                    has_image = True
                    main_image = os.path.basename(image_files[0])  # First image as main
                    if len(image_files) > 1:
                        extra_images = [os.path.basename(f) for f in image_files[1:]]
                    stats['images'] += len(image_files)
                
                # Scan for description files
                desc_extensions = ['*.txt', '*.html', '*.md']
                desc_files = []
                
                for ext in desc_extensions:
                    desc_files.extend(glob.glob(os.path.join(product_folder, ext)))
                
                if desc_files:
                    has_description = True
                    description_file = os.path.basename(desc_files[0])  # First description file
                    stats['descriptions'] += len(desc_files)
            
            # Update database
            update_sql = """
            UPDATE products 
            SET has_image = ?, has_description = ?, main_image_filename = ?, 
                extra_image_filenames = ?, description_filename = ?,
                last_checked_timestamp = ?
            WHERE id = ?
            """
            
            cursor.execute(update_sql, (
                has_image,
                has_description,
                main_image,
                json.dumps(extra_images) if extra_images else None,
                description_file,
                datetime.now().isoformat(),
                product_id
            ))
            
            stats['updated'] += 1
        
        self.connection.commit()
        
        print(f"✅ Filesystem scan complete:")
        print(f"  📁 Updated {stats['updated']} products")
        print(f"  🖼️ Found {stats['images']} images")
        print(f"  📝 Found {stats['descriptions']} descriptions")
        
        return stats
    
    def get_product_by_id(self, product_id):
        """
        Retrieves a single product by ID.
        
        Args:
            product_id (int): Product ID
            
        Returns:
            dict: Product data or None if not found
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except sqlite3.Error as e:
            print(f"❌ Error retrieving product {product_id}: {e}")
            return None
    
    def get_all_products(self, filter_incomplete=False):
        """
        Retrieves all products from the database.
        
        Args:
            filter_incomplete (bool): If True, only return products with images and descriptions
            
        Returns:
            list: List of product dictionaries
        """
        try:
            cursor = self.connection.cursor()
            
            if filter_incomplete:
                cursor.execute("""
                    SELECT * FROM products 
                    WHERE is_active = 1 AND has_image = 1 AND has_description = 1
                    ORDER BY category_path, product_name
                """)
            else:
                cursor.execute("""
                    SELECT * FROM products 
                    WHERE is_active = 1
                    ORDER BY category_path, product_name
                """)
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            print(f"❌ Error retrieving products: {e}")
            return []
    
    def update_product_status(self, product_id, **kwargs):
        """
        Updates product status fields.
        
        Args:
            product_id (int): Product ID
            **kwargs: Fields to update (is_active, is_uploaded, etc.)
            
        Returns:
            bool: True if update successful
        """
        try:
            # Build dynamic update query
            set_clauses = []
            values = []
            
            for field, value in kwargs.items():
                if field in ['is_active', 'is_uploaded', 'has_image', 'has_description']:
                    set_clauses.append(f"{field} = ?")
                    values.append(value)
            
            if not set_clauses:
                return False
            
            # Add timestamp
            set_clauses.append("last_modified_timestamp = ?")
            values.append(datetime.now().isoformat())
            values.append(product_id)
            
            update_sql = f"UPDATE products SET {', '.join(set_clauses)} WHERE id = ?"
            
            cursor = self.connection.cursor()
            cursor.execute(update_sql, values)
            self.connection.commit()
            
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"❌ Error updating product {product_id}: {e}")
            return False
    
    def get_database_stats(self):
        """
        Returns database statistics.
        
        Returns:
            dict: Statistics about the database
        """
        try:
            cursor = self.connection.cursor()
            
            stats = {}
            
            # Total products
            cursor.execute("SELECT COUNT(*) FROM products")
            stats['total_products'] = cursor.fetchone()[0]
            
            # Active products
            cursor.execute("SELECT COUNT(*) FROM products WHERE is_active = 1")
            stats['active_products'] = cursor.fetchone()[0]
            
            # Products with images
            cursor.execute("SELECT COUNT(*) FROM products WHERE has_image = 1")
            stats['products_with_images'] = cursor.fetchone()[0]
            
            # Products with descriptions
            cursor.execute("SELECT COUNT(*) FROM products WHERE has_description = 1")
            stats['products_with_descriptions'] = cursor.fetchone()[0]
            
            # Uploaded products
            cursor.execute("SELECT COUNT(*) FROM products WHERE is_uploaded = 1")
            stats['uploaded_products'] = cursor.fetchone()[0]
            
            # Categories
            cursor.execute("SELECT COUNT(DISTINCT category_path) FROM products WHERE category_path IS NOT NULL")
            stats['categories'] = cursor.fetchone()[0]
            
            return stats
            
        except sqlite3.Error as e:
            print(f"❌ Error getting database stats: {e}")
            return {}
    
    def close(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")

# Test the DataManager if run directly
if __name__ == "__main__":
    print("🧪 Testing DataManager...")
    print("=" * 50)
    
    # Initialize
    dm = DataManager()
    
    # Get stats
    stats = dm.get_database_stats()
    print(f"📊 Database Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test getting products
    products = dm.get_all_products()
    print(f"\n📦 Found {len(products)} products in database")
    
    if products:
        print(f"\n📋 Sample product:")
        sample = products[0]
        for key, value in sample.items():
            print(f"  {key}: {value}")
    
    dm.close()
    print("\n✅ DataManager test complete!")
