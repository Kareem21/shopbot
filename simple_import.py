#!/usr/bin/env python3
"""
Simple Import Script for ShopBot
Directly imports Excel data without CSV conversion step.

Usage:
    python simple_import.py

This script will:
1. Read your Excel file directly
2. Map Hungarian columns to database fields
3. Import all products into the database
"""

import pandas as pd
import sqlite3
from datetime import datetime

def parse_price(price_str):
    """
    Parses price from format "13.990 ; 8990" to extract main price.
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

def build_category_path(row):
    """
    Builds category path from Kategória columns.
    """
    categories = []

    # Check each category column
    for col in ['Kategória', 'Kategória 2', 'Kategória 3']:
        if col in row and pd.notna(row[col]) and str(row[col]).strip():
            categories.append(str(row[col]).strip())

    return ' > '.join(categories) if categories else ''

def parse_parts_count(parts_str):
    """
    Parses parts count from "Részek száma" column.
    """
    if pd.isna(parts_str):
        return 0

    try:
        return int(str(parts_str).strip())
    except (ValueError, AttributeError):
        return 0

def main():
    print("📊 ShopBot Simple Import")
    print("=" * 50)

    # Check if Excel file exists
    excel_path = 'data/products.xlsx'
    try:
        # Read Excel file
        print(f"📋 Reading Excel file: {excel_path}")
        df = pd.read_excel(excel_path, engine='openpyxl')

        # Clean column names
        df.columns = df.columns.str.strip()

        print(f"✅ Read {len(df)} rows from Excel")
        print(f"📋 Columns found: {list(df.columns)}")

        # Connect to database
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        # Clear existing data
        cursor.execute("DELETE FROM products")
        print("🗑️ Cleared existing products from database")

        # Process each row
        processed = 0
        errors = 0

        for index, row in df.iterrows():
            try:
                # Skip rows without product code
                if pd.isna(row.get('Termék kód', '')) or not str(row['Termék kód']).strip():
                    continue

                # Map data
                sku = str(row['Termék kód']).strip()
                product_name = str(row.get('Terméknév', '')).strip()
                category_path = build_category_path(row)
                size_cm = str(row.get('Méret (cm)', '')).strip()
                parts_count = parse_parts_count(row.get('Részek száma'))
                color = str(row.get('Szín', '')).strip()
                material = str(row.get('Anyag', '')).strip()
                thickness = str(row.get('Vastagság', '')).strip()
                price = parse_price(row.get('Ár'))

                # Insert into database
                cursor.execute("""
                    INSERT INTO products (
                        sku, product_name, category_path, size_cm, parts_count,
                        color, material, thickness, price,
                        is_active, created_timestamp, last_modified_timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    sku, product_name, category_path, size_cm, parts_count,
                    color, material, thickness, price,
                    1,  # is_active
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))

                processed += 1
                print(f"  ✅ {sku}: {product_name}")

            except Exception as e:
                errors += 1
                print(f"  ❌ Error processing row {index + 1}: {e}")
                continue

        # Commit changes
        conn.commit()

        # Show results
        print(f"\n📊 Import Results:")
        print(f"✅ Successfully imported: {processed} products")
        if errors > 0:
            print(f"⚠️ Errors: {errors} rows")

        # Verify the import
        cursor.execute("SELECT COUNT(*) FROM products")
        total_count = cursor.fetchone()[0]
        print(f"🗄️ Total products in database: {total_count}")

        # Show sample products
        cursor.execute("SELECT sku, product_name, category_path, price FROM products LIMIT 5")
        sample_products = cursor.fetchall()

        print(f"\n📦 Sample Products:")
        for product in sample_products:
            print(f"  SKU: {product[0]}")
            print(f"      Name: {product[1]}")
            print(f"      Category: {product[2]}")
            print(f"      Price: {product[3]}")
            print()

        conn.close()

        print("🎉 Import completed successfully!")
        print("\nNext steps:")
        print("1. Run 'python main.py' to verify the system")
        print("2. Run 'python data_manager.py' to test data operations")

    except FileNotFoundError:
        print(f"❌ Excel file not found: {excel_path}")
        print("Please make sure your Excel file is at: data/products.xlsx")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("Make sure you have pandas and openpyxl installed:")
        print("  pip install pandas openpyxl")

if __name__ == "__main__":
    main()