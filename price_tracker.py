import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

class NinjagoTracker:
    def __init__(self):
        self.deals = []
        self.price_history = self.load_price_history()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def load_price_history(self):
        """Load previous price data from CSV"""
        if os.path.exists('price_history.csv'):
            history = {}
            with open('price_history.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    key = f"{row['retailer']}_{row['product_id']}"
                    history[key] = float(row['price'])
            return history
        return {}
    
    def save_price_history(self, products):
        """Save current prices to CSV"""
        fieldnames = ['date', 'retailer', 'product_id', 'name', 'price', 'url']
        file_exists = os.path.exists('price_history.csv')
        
        with open('price_history.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            
            for product in products:
                writer.writerow({
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'retailer': product['retailer'],
                    'product_id': product['id'],
                    'name': product['name'],
                    'price': product['price'],
                    'url': product['url']
                })
    
    def check_amazon(self):
        """Scrape Amazon for Ninjago sets"""
        print("Checking Amazon...")
        products = []
        
        try:
            # Amazon search URL for Lego Ninjago
            url = "https://www.amazon.com/s?k=lego+ninjago&i=toys-and-games"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find product containers
            items = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for item in items[:20]:  # Limit to first 20 results
                try:
                    # Extract product details
                    title_elem = item.find('h2', class_='a-size-mini')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Only include if it's actually a Lego Ninjago product
                    if 'ninjago' not in title.lower() or 'lego' not in title.lower():
                        continue
                    
                    # Get price
                    price_elem = item.find('span', class_='a-price-whole')
                    if not price_elem:
                        continue
                    
                    price_text = price_elem.get_text(strip=True).replace(',', '').replace('$', '')
                    price = float(price_text)
                    
                    # Get product URL and ID
                    link = item.find('a', class_='a-link-normal')
                    if not link:
                        continue
                    
                    product_url = "https://www.amazon.com" + link['href']
                    asin = item.get('data-asin', '')
                    
                    products.append({
                        'retailer': 'Amazon',
                        'id': asin,
                        'name': title[:100],  # Truncate long titles
                        'price': price,
                        'url': product_url
                    })
                    
                except Exception as e:
                    print(f"Error parsing Amazon item: {e}")
                    continue
            
            print(f"Found {len(products)} products on Amazon")
            
        except Exception as e:
            print(f"Error checking Amazon: {e}")
        
        return products
    
    def check_walmart(self):
        """Scrape Walmart for Ninjago sets"""
        print("Checking Walmart...")
        products = []
        
        try:
            url = "https://www.walmart.com/search?q=lego+ninjago"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            # Walmart uses dynamic loading, so we'll try to parse what we can
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find product data in JSON
            scripts = soup.find_all('script', type='application/json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    # This is a simplified approach - Walmart's structure changes frequently
                    # In production, you'd need more robust parsing
                except:
                    continue
            
            print(f"Found {len(products)} products on Walmart")
            
        except Exception as e:
            print(f"Error checking Walmart: {e}")
        
        return products
    
    def check_target(self):
        """Scrape Target for Ninjago sets"""
        print("Checking Target...")
        products = []
        
        try:
            url = "https://www.target.com/s?searchTerm=lego+ninjago"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Target also uses dynamic loading
            # This is a placeholder - actual implementation would need API calls
            
            print(f"Found {len(products)} products on Target")
            
        except Exception as e:
            print(f"Error checking Target: {e}")
        
        return products
    
    def check_lego_official(self):
        """Scrape Lego.com for Ninjago sets"""
        print("Checking Lego.com...")
        products = []
        
        try:
            url = "https://www.lego.com/en-us/themes/ninjago"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Lego.com uses dynamic loading
            # This is a placeholder for the structure
            
            print(f"Found {len(products)} products on Lego.com")
            
        except Exception as e:
            print(f"Error checking Lego.com: {e}")
        
        return products
    
    def analyze_deals(self, products):
        """Compare current prices with history to find deals"""
        deals = []
        
        for product in products:
            key = f"{product['retailer']}_{product['id']}"
            current_price = product['price']
            
            # Check if we have historical data
            if key in self.price_history:
                old_price = self.price_history[key]
                
                # Calculate discount percentage
                discount_pct = ((old_price - current_price) / old_price) * 100
                
                # Flag as deal if 15% or more discount
                if discount_pct >= 15:
                    deals.append({
                        **product,
                        'old_price': old_price,
                        'discount_pct': discount_pct
                    })
            else:
                # New product - flag if under $50 (good deals territory)
                if current_price < 50:
                    deals.append({
                        **product,
                        'old_price': None,
                        'discount_pct': None,
                        'note': 'New product found!'
                    })
        
        return deals
    
    def send_email_alert(self, deals):
        """Send email notification about deals"""
        if not deals:
            print("No deals to report")
            return
        
        # Get email credentials from environment variables
        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('SENDER_PASSWORD')
        recipient_email = os.environ.get('RECIPIENT_EMAIL')
        
        if not all([sender_email, sender_password, recipient_email]):
            print("Email credentials not configured. Skipping email notification.")
            print("Deals found:")
            for deal in deals:
                print(f"- {deal['name']} at {deal['retailer']}: ${deal['price']}")
            return
        
        # Create email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🔥 {len(deals)} Lego Ninjago Deal(s) Found!"
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        # Create email body
        html = """
        <html>
        <body>
        <h2>Lego Ninjago Deals Alert!</h2>
        <p>Found the following deals:</p>
        """
        
        for deal in deals:
            discount_text = ""
            if deal.get('old_price'):
                discount_text = f"<br><strong>Was: ${deal['old_price']:.2f} - Save {deal['discount_pct']:.0f}%!</strong>"
            
            html += f"""
            <div style="border: 1px solid #ddd; padding: 10px; margin: 10px 0;">
                <h3>{deal['name']}</h3>
                <p><strong>Retailer:</strong> {deal['retailer']}</p>
                <p><strong>Price:</strong> ${deal['price']:.2f}{discount_text}</p>
                <p><a href="{deal['url']}">View Product</a></p>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        # Send email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
            print(f"Email sent successfully with {len(deals)} deals!")
        except Exception as e:
            print(f"Error sending email: {e}")
    
    def run(self):
        """Main execution method"""
        print(f"Starting Ninjago price check at {datetime.now()}")
        print("-" * 50)
        
        all_products = []
        
        # Check all retailers
        all_products.extend(self.check_amazon())
        time.sleep(2)  # Be polite with requests
        
        all_products.extend(self.check_walmart())
        time.sleep(2)
        
        all_products.extend(self.check_target())
        time.sleep(2)
        
        all_products.extend(self.check_lego_official())
        
        print(f"\nTotal products found: {len(all_products)}")
        
        # Analyze for deals
        deals = self.analyze_deals(all_products)
        print(f"Deals identified: {len(deals)}")
        
        # Save current prices
        if all_products:
            self.save_price_history(all_products)
        
        # Send alert if deals found
        if deals:
            self.send_email_alert(deals)
        
        print("-" * 50)
        print("Price check complete!")
        
        return deals

if __name__ == "__main__":
    tracker = NinjagoTracker()
    tracker.run()
