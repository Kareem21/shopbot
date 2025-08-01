#!/usr/bin/env python3
"""
Create Sample Data Structure for ShopBot
Creates folders, sample images, and Excel file for testing.
"""

import os
import pandas as pd
from PIL import Image
import random

def create_sample_image(filepath, width=800, height=600, color=None):
    """Creates a simple colored rectangle image"""
    if color is None:
        # Random color
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Create image
    img = Image.new('RGB', (width, height), color)

    # Add some simple pattern
    pixels = img.load()
    for i in range(0, width, 50):
        for j in range(0, height, 50):
            if (i + j) % 100 == 0:
                for x in range(i, min(i+10, width)):
                    for y in range(j, min(j+10, height)):
                        pixels[x, y] = (255, 255, 255)  # White dots

    img.save(filepath)
    print(f"✅ Created image: {filepath}")

def create_folders_and_files():
    """Creates the complete folder structure with sample data"""

    print("🚀 Creating ShopBot sample data structure...")

    # Create main directories
    os.makedirs('data/products', exist_ok=True)

    # Sample product data
    products = [
        {
            'sku': 'Földgömb1',
            'name': 'Földgömb puzzle 1',
            'category1': 'Falitérkép',
            'category2': '',
            'category3': '',
            'size': '50 x 50 ; 32 x 32',
            'parts': 2,
            'color': 'Fekete',
            'material': 'HDF',
            'thickness': '3mm',
            'price': '13.990 ; 8990'
        },
        {
            'sku': 'Földgömb2',
            'name': 'Földgömb puzzle 2',
            'category1': 'Falitérkép',
            'category2': '',
            'category3': '',
            'size': '38 x 38 ; 25 x 25',
            'parts': 1,
            'color': 'Fekete',
            'material': 'HDF',
            'thickness': '3mm',
            'price': '13.990 ; 8990'
        },
        {
            'sku': 'Térkép',
            'name': 'Világtérkép puzzle',
            'category1': 'Falitérkép',
            'category2': '',
            'category3': '',
            'size': '126 x 60 ; 82 x 40',
            'parts': 3,
            'color': 'Fekete',
            'material': 'HDF',
            'thickness': '3mm',
            'price': '13.990 ; 8990'
        },
        {
            'sku': 'Mandala1',
            'name': 'Mandala design 1',
            'category1': 'Mandalák',
            'category2': '',
            'category3': '',
            'size': '126 x 60 ; 82 x 40',
            'parts': 3,
            'color': 'Fekete',
            'material': 'HDF',
            'thickness': '3mm',
            'price': '13.990 ; 8990'
        },
        {
            'sku': 'Mandala2',
            'name': 'Mandala design 2',
            'category1': 'Mandalák',
            'category2': '',
            'category3': '',
            'size': '133 x 60 ; 87 x 40',
            'parts': 5,
            'color': 'Fekete',
            'material': 'HDF',
            'thickness': '3mm',
            'price': '13.990 ; 8990'
        },
        {
            'sku': 'Virág1',
            'name': 'Virág minta 1',
            'category1': 'Természet',
            'category2': 'Virágok',
            'category3': '',
            'size': '107 x 60 ; 70 x 40',
            'parts': 3,
            'color': 'Fekete',
            'material': 'HDF',
            'thickness': '3mm',
            'price': '13.990 ; 8990'
        },
        {
            'sku': 'Virág2',
            'name': 'Virág minta 2',
            'category1': 'Természet',
            'category2': 'Virágok',
            'category3': '',
            'size': '120 x 35 ; 78 x 23',
            'parts': 3,
            'color': 'Fekete',
            'material': 'HDF',
            'thickness': '3mm',
            'price': '13.990 ; 8990'
        },
        {
            'sku': 'Egyetem1',
            'name': 'Egyetem logo 1',
            'category1': 'Természet',
            'category2': 'Univerzum',
            'category3': '',
            'size': '38 x 38 ; 25 x 25',
            'parts': 1,
            'color': 'Fekete',
            'material': 'HDF',
            'thickness': '3mm',
            'price': '13.990 ; 8990'
        }
    ]

    # Create product folders and files
    colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100), (255, 100, 255)]

    for i, product in enumerate(products):
        sku = product['sku']
        product_dir = f'data/products/{sku}'
        os.makedirs(product_dir, exist_ok=True)

        # Create sample images
        color = colors[i % len(colors)]
        create_sample_image(f'{product_dir}/image1.jpg', color=color)
        create_sample_image(f'{product_dir}/image2.jpg', width=600, height=800, color=color)

        # Create description file
        description = f"""Termék: {product['name']}
SKU: {sku}
Kategória: {product['category1']}
Méret: {product['size']}
Anyag: {product['material']}
Színek: {product['color']}
Vastagság: {product['thickness']}

Ez egy gyönyörű {product['name'].lower()} puzzle, amely tökéletes dekoráció lehet otthonában.
Kiváló minőségű {product['material']} anyagból készült, {product['thickness']} vastagságban.

Jellemzők:
- Precíz lézervágás
- Környezetbarát anyag
- Könnyű összeszerelés
- Modern design

A csomag {product['parts']} darab puzzle elemet tartalmaz.
"""

        with open(f'{product_dir}/description.txt', 'w', encoding='utf-8') as f:
            f.write(description)

        print(f"✅ Created product folder: {product_dir}")

    # Create Excel file
    print("\n📊 Creating Excel file...")

    excel_data = []
    for product in products:
        excel_data.append({
            'Kategória': product['category1'],
            'Kategória 2': product['category2'],
            'Kategória 3': product['category3'],
            'Termék kód': product['sku'],
            'Terméknév': product['name'],
            'Méret (cm)': product['size'],
            'Részek száma': product['parts'],
            'Szín': product['color'],
            'Anyag': product['material'],
            'Vastagság': product['thickness'],
            'Ár': product['price']
        })

    df = pd.DataFrame(excel_data)
    df.to_excel('data/products.xlsx', index=False)

    print("✅ Created Excel file: data/products.xlsx")

    # Show summary
    print(f"\n🎉 Sample data created successfully!")
    print(f"📦 Created {len(products)} products")
    print(f"🖼️ Created {len(products) * 2} sample images")
    print(f"📝 Created {len(products)} description files")
    print(f"📊 Created Excel file with product data")

    print(f"\n📁 Folder structure:")
    print(f"data/")
    print(f"├── products.xlsx")
    print(f"└── products/")
    for product in products:
        print(f"    ├── {product['sku']}/")
        print(f"    │   ├── image1.jpg")
        print(f"    │   ├── image2.jpg")
        print(f"    │   └── description.txt")

    print(f"\n✅ Ready to run: python main.py")

if __name__ == "__main__":
    try:
        create_folders_and_files()
    except ImportError as e:
        if "PIL" in str(e):
            print("❌ Pillow not installed. Run: pip install Pillow")
        else:
            print(f"❌ Missing dependency: {e}")
            print("Run: pip install pandas openpyxl Pillow")
    except Exception as e:
        print(f"❌ Error: {e}")