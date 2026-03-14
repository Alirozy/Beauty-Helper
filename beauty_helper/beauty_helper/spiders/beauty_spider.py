import scrapy
from beauty_helper.items import ProductItem

class BeautySpider(scrapy.Spider):
    name = "beauty_bot"
    
    # Başlangıç URL'i
    start_urls = [
        'https://www.guzellikdeposu.com/kategori/tum-urunler'
    ]

    def parse(self, response):
        # KRİTİK DÜZELTME: 'div.product-item' yerine 'div.showcase' kullanıyoruz
        products = response.css('div.showcase')
        
        for product in products:
            item = ProductItem()
            
            # Başlık: .showcase-title içindeki a etiketinin metni
            item['name'] = product.css('.showcase-title a::text').get()
            
            # Fiyat: .showcase-price-new içindeki metni al ve boşlukları temizle
            price = product.css('.showcase-price-new::text').get()
            item['price'] = price.strip() if price else None
            
            # Görsel: .showcase-image içindeki img etiketinin src veya data-src özelliği
            # Bazı siteler hız için 'data-src' kullanır, garantiye almak için kontrol ediyoruz
            img_url = product.css('.showcase-image img::attr(data-src)').get() or \
                      product.css('.showcase-image img::attr(src)').get()
            item['poster_url'] = response.urljoin(img_url) if img_url else None
            
            # Ürün linki
            product_url = product.css('.showcase-title a::attr(href)').get()
            item['url'] = response.urljoin(product_url) if product_url else response.url
            
            # Sadece ismi olan ürünleri gönder (boş verileri engeller)
            if item['name']:
                yield item

        # SAYFALANDIRMA (PAGINATION)
        # Senin görseldeki sağ ok ikonuna sahip linki bulur
        next_page = response.css('a:has(i.fa-chevron-right)::attr(href)').get()

        if next_page and "javascript" not in next_page:
            next_url = response.urljoin(next_page)
            # Sayfa geçişi yaparken bir log düşelim ki çalıştığını görelim
            self.logger.info(f"Sonraki sayfaya gidiliyor: {next_url}")
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            self.logger.info("Tüm sayfalar tarandı veya sonraki sayfa linki bulunamadı.")