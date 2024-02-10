import sqlite3
import random

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                codigo INTEGER PRIMARY KEY,
                codebar TEXT UNIQUE,
                produto TEXT UNIQUE,
                desc_produto TEXT,
                cor_produto TEXT,
                tamanho TEXT
            )
        ''')
        self.conn.commit()

    def generate_random_product(self):
        codebar = ''.join(random.choices('0123456789', k=12))
        produto = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
        desc_produto = random.choice(["Camiseta", "Calça", "Vestido", "Camisa", "Blusa", "Saia", "Jaqueta", "Blazer", "Shorts", "Macacão"])
        desc_produto += " " + random.choice(["de algodão", "de linho", "de seda", "de lã", "de jeans", "estampada", "bordada", "com listras", "com estampa floral"])
        cor_produto = random.choice(["Preto", "Branco", "Azul", "Vermelho", "Verde", "Amarelo", "Rosa", "Roxo", "Cinza", "Marrom"])
        tamanho = random.choice(["P", "M", "G", "GG", "XGG"])
        return (codebar, produto, desc_produto, cor_produto, tamanho)

    def insert_random_products(self, num_records):
        for _ in range(num_records):
            record = self.generate_random_product()
            self.cursor.execute('''
                INSERT INTO produtos (codebar, produto, desc_produto, cor_produto, tamanho) 
                VALUES (?, ?, ?, ?, ?)
            ''', record)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    db_manager = DatabaseManager('codigobarras.db')
    db_manager.create_table()
    db_manager.insert_random_products(100)
    db_manager.close_connection()
