import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT


def get_db_connection():
    conn = None
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f'Ошибка подключения к базе данных: {e}')
        if conn is not None:
            conn.close()
        raise e
