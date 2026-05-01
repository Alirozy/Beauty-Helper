import scrapy
from beauty_helper.items import ProductItem
from urllib.parse import urlparse

class BeautySpider(scrapy.Spider):
    name = "beauty_bot"
    
    # STEP 1: Define scraping rules for each target domain
    site_config = {
        'www.guzellikdeposu.com': {
            'container': 'div.showcase',
            'name': '.showcase-title a::text',
            'price': '.showcase-price-new::text',
            'image': '.showcase-image img::attr(data-src), .showcase-image img::attr(src)',
            'stock_status': '.sold-out-label span::text',
            'next_page': 'a:has(i.fa-chevron-right)::attr(href)'
        },
    }

    # STEP 2: Define starting URLs
    start_urls = [
            'https://www.guzellikdeposu.com/kategori/tum-urunler',
    ]       

    def parse(self, response):
        # Identify the domain to apply the correct rules
        domain = urlparse(response.url).netloc
        rules = self.site_config.get(domain)

        if not rules:
            self.logger.error(f"No configuration found for domain: {domain}")
            return

        # Locate all product containers on the page
        products = response.css(rules['container'])
        
        for product in products:
            item = ProductItem()
            
            # 1. SCRAPE PRODUCT NAME
            name = product.css(rules['name']).get()
            item['name'] = name.strip() if name else None

            # 2. SCRAPE PRICE
            price_selector = rules.get('price', '')
            raw_price = product.css(price_selector).get()
            if "tl" in raw_price.lower():
                item['currency'] = 'TRY'
                raw_price = raw_price.lower().replace('tl', '').strip()
                item['price'] = raw_price if raw_price else None

            # 3. SCRAPE RATING (SVG Star Counting)
            if 'rating' in rules:
                filled_stars = product.css(rules['rating']).getall()
                rating_score = len(filled_stars)
                item['rating'] = f"{rating_score} / 5 Stars" if rating_score > 0 else "No Rating"
            else:
                item['rating'] = "Rating N/A"

            # 6. SCRAPE STOCK STATUS
            stock_selector = rules.get('stock_status')
            if stock_selector:
                raw_stock = product.css(stock_selector).get()
                
                if domain == 'www.guzellikdeposu.com':
                    # If "Tükendi" label exists, it is Out of Stock
                    item['stock'] = "Out of Stock" if raw_stock else "In Stock"
                else:
                    # For Panter and others, use found text or default to In Stock
                    item['stock'] = raw_stock.strip() if raw_stock else "In Stock"
            else:
                item['stock'] = "In Stock"

            # 4. SCRAPE PRODUCT IMAGE
            image_url = None
            # Support for multiple attribute fallbacks (e.g., data-src or src)
            selectors = rules['image'].split(',')
            for sel in selectors:
                image_url = product.css(sel.strip()).get()
                if image_url: 
                    break
            item['poster_url'] = response.urljoin(image_url) if image_url else None
            
            # 5. SCRAPE PRODUCT URL
            link = product.css('a::attr(href)').get()
            item['stores_url'] = response.urljoin(link) if link else response.url
            
            # Fill missing fields defined in items.py
            item['brand'] = None
            item['website'] = domain
            item['type'] = None
            item['description'] = None
            item['production_year'] = None

            if domain == 'www.guzellikdeposu.com':
                item['stores_name'] = 'Güzellik Deposu'
#            elif domain == 'panterkozmetik.com':
#                item['stores_name'] = 'Panter Kozmetik'
            else:
                item['stores_name'] = domain
            
            # Yield item only if it has a valid name
            if item['name']:
                yield item

        # 6. PAGINATION (Handle "Next Page")
        next_page_link = response.css(rules['next_page']).get()
        if next_page_link and "javascript" not in next_page_link:
            target_url = response.urljoin(next_page_link)
            yield scrapy.Request(target_url, callback=self.parse)