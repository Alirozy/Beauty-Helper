import psycopg2
import os
from pathlib import Path
from dotenv import load_dotenv

class BeautyHelperPipeline:
    def __init__(self):
        # 1. Load the .env file from the root directory (3 folders up)
        base_dir = Path(__file__).resolve().parent.parent.parent
        env_path = base_dir / '.env'
        load_dotenv(dotenv_path=env_path)

        # 2. Assign variables (with default values)
        self.hostname = os.getenv('DB_HOST', 'localhost')
        self.username = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
        self.port = os.getenv('DB_PORT', '5432')
        
        self.connection = None
        self.cur = None

    def open_spider(self, spider):
        """Establishes DB connection and prepares tables when Spider starts."""
        try:
            self.connection = psycopg2.connect(
                host=self.hostname,
                user=self.username,
                password=self.password,
                dbname=self.database,
                port=self.port
            )
            self.cur = self.connection.cursor()
            self._create_tables()
            spider.log(f"PostgreSQL connection successful: {self.database}")
        except Exception as e:
            spider.log(f"Database connection error: {e}")
            raise e

    def _create_tables(self):
        """Creates tables sequentially with relationships."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS Brands(
                id SERIAL PRIMARY KEY,
                brand VARCHAR(255) UNIQUE NOT NULL,
                website VARCHAR(255)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Products(
                id SERIAL PRIMARY KEY,
                brand_id INT REFERENCES Brands(id) ON DELETE CASCADE,
                name VARCHAR(500) UNIQUE NOT NULL,
                type VARCHAR(255),
                description TEXT,
                production_year VARCHAR(50),
                poster_url TEXT,
                rating VARCHAR(50)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS Product_Sources(
                id SERIAL PRIMARY KEY,
                product_id INT REFERENCES Products(id) ON DELETE CASCADE,
                store_name VARCHAR(255),
                store_url TEXT UNIQUE NOT NULL,
                price VARCHAR(100),
                currency VARCHAR(50),
                stock VARCHAR(50)
            )
            """
        ]
        for query in queries:
            self.cur.execute(query)
        self.connection.commit()

    def process_item(self, item, spider):
        """Cleans the data and saves it to PostgreSQL atomically."""
        try:
            # --- 1. Brand Operation ---
            brand_val = item.get('brand') or 'Unknown'
            self.cur.execute("""
                INSERT INTO Brands (brand, website)
                VALUES (%s, %s)
                ON CONFLICT (brand) DO UPDATE SET website = EXCLUDED.website
                RETURNING id;
            """, (brand_val, item.get('website', '')))
            brand_id = self.cur.fetchone()[0]

            # --- 2. Product Operation ---
            name_val = item.get('name') or 'Unknown Product'
            self.cur.execute("""
                INSERT INTO Products (brand_id, name, type, description, production_year, poster_url, rating)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE SET
                    brand_id = EXCLUDED.brand_id,
                    type = EXCLUDED.type,
                    description = EXCLUDED.description,
                    production_year = EXCLUDED.production_year,
                    poster_url = EXCLUDED.poster_url,
                    rating = EXCLUDED.rating
                RETURNING id;
            """, (
                brand_id, name_val, 
                item.get('type'), item.get('description'), 
                item.get('production_year'), item.get('poster_url'), 
                item.get('rating')
            ))
            product_id = self.cur.fetchone()[0]

            # --- 3. Source Operation ---
            self.cur.execute("""
                INSERT INTO Product_Sources (product_id, store_name, store_url, price, currency, stock)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (store_url) DO UPDATE SET
                    product_id = EXCLUDED.product_id,
                    store_name = EXCLUDED.store_name,
                    price = EXCLUDED.price,
                    currency = EXCLUDED.currency,
                    stock = EXCLUDED.stock;
            """, (
                product_id,
                item.get('stores_name'),
                item.get('stores_url'),
                item.get('price'),
                item.get('currency'),
                item.get('stock')
            ))

            self.connection.commit()
        except Exception as e:
            self.connection.rollback() # Rollback the operation if an error occurs
            spider.log(f"Data write error: {e}")
        
        return item

    def close_spider(self, spider):
        """Closes connections securely."""
        if self.cur:
            self.cur.close()
        if self.connection:
            self.connection.close()