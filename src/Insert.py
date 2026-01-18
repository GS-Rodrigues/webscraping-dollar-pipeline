import psycopg2

def insert_row(cursor, data_referencia, value_purchase, value_selling):
    try:
        cursor.execute("""
            INSERT INTO valores_scraping_lme (data_referencia, valor_compra, valor_venda)
            VALUES (%s, %s, %s)
            ON CONFLICT (data_referencia) DO UPDATE
            SET
                valor_venda = EXCLUDED.valor_venda,
                valor_compra = EXCLUDED.valor_compra;
        """, (data_referencia, value_purchase, value_selling))

    except psycopg2.Error as e:
        print("Erro ao inserir no banco:", e)

