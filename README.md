# ShopBot - E-commerce Product Management System

A comprehensive Python application for managing e-commerce products with web automation capabilities.

## 🚀 Quick Start (WebStorm IDE)

### Step 1: Setup Project in WebStorm

1. **Create New Project:**
   - Open WebStorm
   - File → New → Project
   - Choose "Pure Python" 
   - Select your project location
   - Choose Python interpreter (3.8+)

2. **Add Files to Project:**
   - Copy all the provided files into your project folder:
     - `main.py`
     - `database_setup.py`
     - `data_manager.py`
     - `bot_driver.py`
     - `config.json`
     - `requirements.txt`
     - `setup.py`

### Step 2: Install Dependencies

**Option A: Using WebStorm's Terminal**
```bash
# Open Terminal in WebStorm (Alt+F12)
pip install -r requirements.txt
playwright install chromium
```

**Option B: Using WebStorm's Package Manager**
1. File → Settings → Project → Python Interpreter
2. Click the "+" button to add packages
3. Install: `pandas`, `openpyxl`, `playwright`, `PyQt5`

### Step 3: Initial Setup

**Run the automated setup:**
```bash
python setup.py
```

**Or manually set up:**
```bash
# 1. Create database
python database_setup.py

# 2. Create directories
mkdir -p data/products chrome_profile logs backups
```

### Step 4: Prepare Your Data

1. **Place your Excel file** at `data/products.xlsx`
2. **Create product folders** in `data/products/[SKU]/`
3. **Add images and descriptions** to each product folder

**Expected folder structure:**
```
shopbot/
├── main.py
├── database_setup.py
├── data_manager.py
├── bot_driver.py
├── config.json
├── products.db
└── data/
    ├── products.xlsx          # Your Excel file
    └── products/
        ├── Földgömb1/         # Product folders (by SKU)
        │   ├── image1.jpg
        │   ├── image2.jpg
        │   └── description.txt
        ├── Mandala1/
        │   └── ...
        └── ...
```

### Step 5: Import and Test

**Import your Excel data:**
```python
# Run this in WebStorm's Python Console or create a script
from data_manager import DataManager
dm = DataManager()

# Convert Excel to CSV
dm.convert_xlsx_to_csv('data/products.xlsx', 'data/products.csv')

# Import to database
dm.sync_csv_to_db('data/products.csv')

# Scan for images/descriptions
dm.scan_and_sync_filesystem('data/products')

dm.close()
```

**Test the system:**
```bash
python main.py
```

## 🏗️ Architecture Overview

### Phase 1: Backend Foundation (✅ COMPLETE)

**Files:**
- `database_setup.py` - Creates SQLite database with product schema
- `data_manager.py` - Handles all data operations and file system scanning
- `bot_driver.py` - Web automation using Playwright
- `config.json` - Application configuration

**Key Features:**
- **Database Schema** matches your Hungarian Excel columns exactly
- **Category Path Building** combines "Kategória" + "Kategória 2" + "Kategória 3"
- **Price Parsing** handles "13.990 ; 8990" format
- **File System Integration** scans for images and descriptions
- **Web Automation** ready for e-commerce site integration

### Phase 2: GUI (⏳ READY FOR DEVELOPMENT)
- PyQt main window with tabbed interface
- Control panel with automation buttons
- Database manager with product browser
- Image preview and management

### Phase 3: Integration (⏳ WAITING)
- Drag & drop functionality
- Threading for long-running tasks
- Full automation workflow

## 🔧 WebStorm Configuration

### Running Files in WebStorm

1. **Right-click any .py file** → "Run 'filename'"
2. **Or use the terminal:**
   ```bash
   python database_setup.py    # Set up database
   python main.py             # Run main application
   python -c "from data_manager import DataManager; dm = DataManager(); print('Test'); dm.close()"
   ```

### Setting Up Run Configurations

1. **Run → Edit Configurations**
2. **Add New Configuration** → Python
3. **Configure:**
   - **Name:** "ShopBot Main"
   - **Script path:** `/path/to/your/main.py`
   - **Working directory:** Your project root
   - **Python interpreter:** Your project interpreter

### Debugging

1. **Set breakpoints** by clicking in the left margin
2. **Right-click file** → "Debug 'filename'"
3. **Use the debugger console** to inspect variables

## 📊 Your Excel File Format

Your Excel file should have these exact Hungarian column names:

| Column | Hungarian Name | Purpose |
|--------|---------------|---------|
| Category 1 | Kategória | Main category |
| Category 2 | Kategória 2 | Subcategory |
| Category 3 | Kategória 3 | Sub-subcategory |
| Product Code | Termék kód | Unique SKU |
| Product Name | Terméknév | Product name |
| Size | Méret (cm) | Dimensions |
| Parts Count | Részek száma | Number of parts |
| Color | Szín | Color |
| Material | Anyag | Material |
| Thickness | Vastagság | Thickness |
| Price | Ár | Price (format: "13.990 ; 8990") |

## 🤖 Web Automation Setup

### Configure for Your E-commerce Site

Edit `bot_driver.py` and customize:

1. **Login selectors** for your site's login form
2. **Product form selectors** for product upload
3. **Category selection logic** for your site's category system
4. **Upload verification checks**

### Update Configuration

Edit `config.json`:
```json
{
  "ecommerce": {
    "site_url": "https://your-ecommerce-site.com",
    "login_url": "https://your-ecommerce-site.com/admin/login",
    "upload_url": "https://your-ecommerce-site.com/admin/products/upload"
  }
}
```

## 🧪 Testing

### Test Individual Components

```bash
# Test database
python database_setup.py

# Test data manager
python data_manager.py

# Test bot driver (requires Playwright setup)
python bot_driver.py

# Test full system
python main.py
```

### Common Issues

1. **"Playwright not found"**
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. **"Database file not found"**
   ```bash
   python database_setup.py
   ```

3. **"Excel file not found"**
   - Place your Excel file at `data/products.xlsx`

4. **"Permission denied"**
   - Check file permissions in your project folder

## 📈 Development Workflow

### Typical Development Session

1. **Open WebStorm** with your ShopBot project
2. **Make changes** to any Python file
3. **Test changes** by running the specific file
4. **Debug issues** using WebStorm's debugger
5. **Run full system test** with `python main.py`

### Adding New Features

1. **Modify the appropriate module:**
   - Database changes → `database_setup.py`
   - Data operations → `data_manager.py`
   - Web automation → `bot_driver.py`
   - Main logic → `main.py`

2. **Test your changes:**
   ```bash
   python your_modified_file.py
   ```

3. **Update configuration** if needed in `config.json`

## 🚀 Next Steps

1. **Complete Phase 1 testing** with your actual data
2. **Customize bot_driver.py** for your e-commerce site
3. **Ready for Phase 2** GUI development
4. **Plan Phase 3** integration features

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify all files are in the correct locations
3. Ensure your Excel file matches the expected format
4. Test each component individually

The system is designed to be modular - each file can be tested independently!
