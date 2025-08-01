# ShopBot - E-commerce Product Manager

Python app for managing e-commerce products with web automation.

## Setup

**Install dependencies:**
```bash
pip install pandas openpyxl playwright
playwright install chromium
```

**Create database:**
```bash
python database_setup.py
```

**Create folders:**
```bash
mkdir -p data/products chrome_profile logs backups
```

## Import Your Data

Put your Excel file at `data/products.xlsx` with these Hungarian columns:
- Kategória, Kategória 2, Kategória 3
- Termék kód, Terméknév  
- Méret (cm), Részek száma
- Szín, Anyag, Vastagság, Ár

**Import to database:**
```bash
python simple_import.py
```

Or use the data manager:
```bash
python -c "from data_manager import DataManager; dm = DataManager(); dm.convert_xlsx_to_csv('data/products.xlsx', 'data/products.csv'); dm.sync_csv_to_db('data/products.csv'); dm.close()"
```

## File Structure

```
shopbot/
├── main.py                 # Main app
├── database_setup.py       # Creates database
├── data_manager.py         # Data operations
├── bot_driver.py          # Web automation
├── simple_import.py       # Easy Excel import
├── config.json            # Settings
├── products.db           # SQLite database
└── data/
    ├── products.xlsx     # Your Excel file
    └── products/         # Product folders
        ├── SKU001/
        │   ├── image1.jpg
        │   └── description.txt
        └── SKU002/
```

## Usage

**Test everything:**
```bash
python main.py
```

**Check data:**
```bash
python data_manager.py
```

## Product Files

Create folders named by SKU in `data/products/`. Add images and `description.txt` files. Run this to scan for files:

```bash
python -c "from data_manager import DataManager; dm = DataManager(); dm.scan_and_sync_filesystem('data/products'); dm.close()"
```

## Configuration

Edit `config.json` for your e-commerce site URLs and settings.

## Current Status

- Backend: Complete
- GUI: Not implemented yet  
- Web automation: Basic framework ready

The system handles Hungarian Excel data and maps it to an English database schema automatically.
