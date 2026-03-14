# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BeautyHelperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Strip whitespaces from all string fields
        for field_name in adapter.field_names():
            value = adapter.get(field_name)
            if isinstance(value, str):
                adapter[field_name] = value.strip()
                
        # Basic price cleaning if it exists
        if adapter.get('price'):
            try:
                # Sadece $, \n ve ekstra boşlukları/yazıları temizle.
                # Virgülü silmiyoruz çünkü TL'de ondalık ayırıcı olarak kullanılıyor (örn: 124,50)
                clean_price = adapter['price'].replace('$', '').replace('\n', '').strip()
                # ' TL' ve 'TL' yazılarını silebiliriz istersen
                if clean_price.endswith('TL'):
                    clean_price = clean_price.replace('TL', '').strip()
                adapter['price'] = clean_price
            except Exception:
                pass
                
        return item
