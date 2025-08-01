#!/usr/bin/env python3
"""
Bot Driver Module for ShopBot
Handles all web automation tasks using Playwright.

This module manages:
- Browser connection and control
- E-commerce site login
- Product upload automation
- Product download/synchronization

Usage:
    from bot_driver import BotDriver
    bot = BotDriver("path/to/chrome/profile")
    bot.connect_to_browser()
    bot.login("username", "password")
"""

import asyncio
import json
import os
import time
from datetime import datetime
from pathlib import Path

# Playwright imports (will be installed separately)
try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright not installed. Run: pip install playwright")

class BotDriver:
    """
    Manages web automation for the ShopBot application.
    
    Handles browser control, login, and product management on e-commerce sites.
    """
    
    def __init__(self, chrome_profile_path="chrome_profile", headless=False):
        """
        Initialize the BotDriver with browser settings.
        
        Args:
            chrome_profile_path (str): Path to Chrome user profile
            headless (bool): Whether to run browser in headless mode
        """
        self.chrome_profile_path = chrome_profile_path
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.is_connected = False
        self.login_status = False
        
        # Configuration
        self.timeout = 30000  # 30 seconds
        self.retry_attempts = 3
        
        print(f"🤖 BotDriver initialized")
        print(f"   Profile: {chrome_profile_path}")
        print(f"   Headless: {headless}")
    
    async def connect_to_browser(self):
        """
        Launches or connects to the persistent Chrome instance.
        
        Returns:
            bool: True if connection successful
        """
        if not PLAYWRIGHT_AVAILABLE:
            print("❌ Cannot connect - Playwright not available")
            return False
        
        try:
            print("🚀 Starting browser connection...")
            
            # Create profile directory if it doesn't exist
            os.makedirs(self.chrome_profile_path, exist_ok=True)
            
            # Launch Playwright
            self.playwright = await async_playwright().start()
            
            # Launch persistent browser context
            self.context = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.chrome_profile_path,
                headless=self.headless,
                viewport={'width': 1920, 'height': 1080},
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            # Create new page
            self.page = await self.context.new_page()
            
            # Set reasonable timeouts
            self.page.set_default_timeout(self.timeout)
            
            self.is_connected = True
            print("✅ Browser connected successfully")
            
            return True
            
        except Exception as e:
            print(f"❌ Browser connection failed: {e}")
            await self.disconnect()
            return False
    
    async def login(self, username, password, login_url=None):
        """
        Logs into the e-commerce admin panel.
        
        Args:
            username (str): Login username
            password (str): Login password
            login_url (str): Login page URL (optional)
            
        Returns:
            bool: True if login successful
        """
        if not self.is_connected:
            print("❌ Cannot login - browser not connected")
            return False
        
        try:
            print(f"🔐 Attempting login for user: {username}")
            
            # Use provided URL or default
            if not login_url:
                login_url = "https://example-shop.com/admin/login"
            
            # Navigate to login page
            await self.page.goto(login_url)
            print(f"📍 Navigated to: {login_url}")
            
            # Wait for login form to load
            await self.page.wait_for_load_state('networkidle')
            
            # Common login form selectors (customize for your site)
            username_selectors = [
                'input[name="username"]',
                'input[name="email"]', 
                'input[type="email"]',
                '#username',
                '#email'
            ]
            
            password_selectors = [
                'input[name="password"]',
                'input[type="password"]',
                '#password'
            ]
            
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign in")'
            ]
            
            # Find and fill username
            username_filled = False
            for selector in username_selectors:
                try:
                    await self.page.wait_for_selector(selector, timeout=5000)
                    await self.page.fill(selector, username)
                    print(f"✅ Username filled using: {selector}")
                    username_filled = True
                    break
                except:
                    continue
            
            if not username_filled:
                print("❌ Could not find username field")
                return False
            
            # Find and fill password
            password_filled = False
            for selector in password_selectors:
                try:
                    await self.page.wait_for_selector(selector, timeout=5000)
                    await self.page.fill(selector, password)
                    print(f"✅ Password filled using: {selector}")
                    password_filled = True
                    break
                except:
                    continue
            
            if not password_filled:
                print("❌ Could not find password field")
                return False
            
            # Find and click submit button
            submit_clicked = False
            for selector in submit_selectors:
                try:
                    await self.page.wait_for_selector(selector, timeout=5000)
                    await self.page.click(selector)
                    print(f"✅ Submit clicked using: {selector}")
                    submit_clicked = True
                    break
                except:
                    continue
            
            if not submit_clicked:
                print("❌ Could not find submit button")
                return False
            
            # Wait for navigation after login
            await self.page.wait_for_load_state('networkidle')
            
            # Check if login was successful (customize this check)
            current_url = self.page.url
            if 'login' not in current_url.lower():
                self.login_status = True
                print("✅ Login successful!")
                return True
            else:
                print("❌ Login failed - still on login page")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    async def upload_new_products(self, products_to_upload):
        """
        Uploads new products to the e-commerce site.
        
        Args:
            products_to_upload (list): List of product dictionaries
            
        Returns:
            dict: Upload results with success/failure counts
        """
        if not self.is_connected or not self.login_status:
            print("❌ Cannot upload - not connected or not logged in")
            return {'success': 0, 'failed': 0, 'errors': []}
        
        print(f"📤 Starting upload of {len(products_to_upload)} products...")
        
        results = {'success': 0, 'failed': 0, 'errors': []}
        
        for i, product in enumerate(products_to_upload, 1):
            try:
                print(f"📦 Uploading product {i}/{len(products_to_upload)}: {product.get('product_name', 'Unknown')}")
                
                # Navigate to product creation page
                await self.page.goto("https://example-shop.com/admin/products/new")
                await self.page.wait_for_load_state('networkidle')
                
                # Fill product form (customize selectors for your site)
                await self._fill_product_form(product)
                
                # Upload images if available
                if product.get('has_image'):
                    await self._upload_product_images(product)
                
                # Submit product
                await self.page.click('button[type="submit"]')
                await self.page.wait_for_load_state('networkidle')
                
                # Check if upload was successful
                if await self._verify_product_upload():
                    results['success'] += 1
                    print(f"✅ Product uploaded successfully")
                else:
                    results['failed'] += 1
                    results['errors'].append(f"Upload verification failed for {product.get('sku', 'unknown')}")
                
                # Small delay between uploads
                await asyncio.sleep(2)
                
            except Exception as e:
                results['failed'] += 1
                error_msg = f"Upload failed for {product.get('sku', 'unknown')}: {e}"
                results['errors'].append(error_msg)
                print(f"❌ {error_msg}")
        
        print(f"📊 Upload complete: {results['success']} success, {results['failed']} failed")
        return results
    
    async def _fill_product_form(self, product):
        """
        Helper method to fill product form fields.
        
        Args:
            product (dict): Product data
        """
        # Product name
        await self.page.fill('input[name="name"]', product.get('product_name', ''))
        
        # SKU
        await self.page.fill('input[name="sku"]', product.get('sku', ''))
        
        # Price
        if product.get('price'):
            await self.page.fill('input[name="price"]', str(product['price']))
        
        # Description
        if product.get('description_filename'):
            description = await self._load_product_description(product)
            await self.page.fill('textarea[name="description"]', description)
        
        # Category (this would need site-specific implementation)
        if product.get('category_path'):
            await self._select_category(product['category_path'])
    
    async def _upload_product_images(self, product):
        """
        Helper method to upload product images.
        
        Args:
            product (dict): Product data with image information
        """
        try:
            # Construct image path
            image_folder = f"data/products/{product['sku']}"
            
            if product.get('main_image_filename'):
                main_image_path = os.path.join(image_folder, product['main_image_filename'])
                if os.path.exists(main_image_path):
                    # Upload main image
                    await self.page.set_input_files('input[type="file"][name="main_image"]', main_image_path)
            
            # Upload additional images if available
            if product.get('extra_image_filenames'):
                extra_images = json.loads(product['extra_image_filenames'])
                for image_name in extra_images:
                    image_path = os.path.join(image_folder, image_name)
                    if os.path.exists(image_path):
                        await self.page.set_input_files('input[type="file"][name="extra_images"]', image_path)
        
        except Exception as e:
            print(f"⚠️ Image upload error: {e}")
    
    async def _load_product_description(self, product):
        """
        Loads product description from file.
        
        Args:
            product (dict): Product data
            
        Returns:
            str: Product description
        """
        try:
            desc_path = f"data/products/{product['sku']}/{product['description_filename']}"
            if os.path.exists(desc_path):
                with open(desc_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"⚠️ Description load error: {e}")
        
        return ""
    
    async def _select_category(self, category_path):
        """
        Selects product category from dropdown/tree.
        
        Args:
            category_path (str): Category path like "Természet/Virágok"
        """
        # This would need to be customized for your specific site's category system
        print(f"📂 Setting category: {category_path}")
        # Implementation would depend on the site's category selection UI
    
    async def _verify_product_upload(self):
        """
        Verifies that product upload was successful.
        
        Returns:
            bool: True if upload successful
        """
        try:
            # Look for success indicators (customize for your site)
            success_indicators = [
                'text="Product created successfully"',
                'text="Product saved"',
                '.success-message',
                '.alert-success'
            ]
            
            for indicator in success_indicators:
                try:
                    await self.page.wait_for_selector(indicator, timeout=5000)
                    return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"⚠️ Upload verification error: {e}")
            return False
    
    async def download_new_products(self):
        """
        Downloads/syncs products from the e-commerce site.
        
        Returns:
            list: List of downloaded product data
        """
        if not self.is_connected or not self.login_status:
            print("❌ Cannot download - not connected or not logged in")
            return []
        
        print("📥 Starting product download from site...")
        
        try:
            # Navigate to products list
            await self.page.goto("https://example-shop.com/admin/products")
            await self.page.wait_for_load_state('networkidle')
            
            # Extract product data from the page
            products = await self.page.evaluate("""
                () => {
                    // This would need to be customized for your site's HTML structure
                    const productRows = document.querySelectorAll('.product-row');
                    const products = [];
                    
                    productRows.forEach(row => {
                        const product = {
                            sku: row.querySelector('.sku')?.textContent?.trim(),
                            name: row.querySelector('.name')?.textContent?.trim(),
                            price: row.querySelector('.price')?.textContent?.trim(),
                            status: row.querySelector('.status')?.textContent?.trim()
                        };
                        
                        if (product.sku) {
                            products.push(product);
                        }
                    });
                    
                    return products;
                }
            """)
            
            print(f"✅ Downloaded {len(products)} products from site")
            return products
            
        except Exception as e:
            print(f"❌ Download error: {e}")
            return []
    
    async def get_browser_status(self):
        """
        Gets current browser and connection status.
        
        Returns:
            dict: Status information
        """
        return {
            'connected': self.is_connected,
            'logged_in': self.login_status,
            'profile_path': self.chrome_profile_path,
            'headless': self.headless,
            'current_url': self.page.url if self.page else None
        }
    
    async def take_screenshot(self, path="screenshot.png"):
        """
        Takes a screenshot of the current page.
        
        Args:
            path (str): Path to save screenshot
            
        Returns:
            bool: True if screenshot taken successfully
        """
        if not self.page:
            return False
        
        try:
            await self.page.screenshot(path=path)
            print(f"📸 Screenshot saved: {path}")
            return True
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            return False
    
    async def disconnect(self):
        """
        Disconnects from the browser and cleans up resources.
        """
        try:
            print("🔌 Disconnecting from browser...")
            
            if self.context:
                await self.context.close()
            
            if self.playwright:
                await self.playwright.stop()
            
            self.is_connected = False
            self.login_status = False
            self.page = None
            self.context = None
            self.browser = None
            self.playwright = None
            
            print("✅ Browser disconnected successfully")
            
        except Exception as e:
            print(f"⚠️ Disconnect error: {e}")

# Synchronous wrapper for easier use
class BotDriverSync:
    """
    Synchronous wrapper for BotDriver to make it easier to use in GUI applications.
    """
    
    def __init__(self, chrome_profile_path="chrome_profile", headless=False):
        self.bot = BotDriver(chrome_profile_path, headless)
        self.loop = None
    
    def _run_async(self, coro):
        """
        Runs an async coroutine in the event loop.
        """
        if self.loop is None:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        
        return self.loop.run_until_complete(coro)
    
    def connect_to_browser(self):
        return self._run_async(self.bot.connect_to_browser())
    
    def login(self, username, password, login_url=None):
        return self._run_async(self.bot.login(username, password, login_url))
    
    def upload_new_products(self, products):
        return self._run_async(self.bot.upload_new_products(products))
    
    def download_new_products(self):
        return self._run_async(self.bot.download_new_products())
    
    def get_browser_status(self):
        return self._run_async(self.bot.get_browser_status())
    
    def take_screenshot(self, path="screenshot.png"):
        return self._run_async(self.bot.take_screenshot(path))
    
    def disconnect(self):
        return self._run_async(self.bot.disconnect())

# Test the BotDriver if run directly
if __name__ == "__main__":
    print("🧪 Testing BotDriver...")
    print("=" * 50)
    
    async def test_bot():
        # Initialize bot
        bot = BotDriver(headless=True)  # Use headless for testing
        
        # Test connection
        connected = await bot.connect_to_browser()
        if connected:
            print("✅ Browser connection test passed")
            
            # Test navigation
            await bot.page.goto("https://httpbin.org/html")
            print("✅ Navigation test passed")
            
            # Test screenshot
            await bot.take_screenshot("test_screenshot.png")
            
            # Get status
            status = await bot.get_browser_status()
            print(f"📊 Browser Status: {status}")
            
        else:
            print("❌ Browser connection test failed")
        
        # Cleanup
        await bot.disconnect()
    
    if PLAYWRIGHT_AVAILABLE:
        asyncio.run(test_bot())
        print("\n✅ BotDriver test complete!")
        print("\nNext steps:")
        print("1. Install Playwright: pip install playwright")
        print("2. Install browsers: playwright install chromium")
        print("3. Customize login/upload methods for your e-commerce site")
    else:
        print("\n⚠️ Cannot test - Playwright not installed")
        print("Run: pip install playwright && playwright install chromium")
