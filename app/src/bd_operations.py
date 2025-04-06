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

def db_table_val(telegram_id: int, first_name: str, username: str, cursor, conn):
	cursor.execute('''
    INSERT INTO users (telegram_id, firstname, username) 
    VALUES (%s, %s, %s)
    ON CONFLICT (telegram_id) 
    DO UPDATE SET 
        firstname = EXCLUDED.firstname,
        username = EXCLUDED.username
''', (telegram_id, first_name, username))
	conn.commit()
     
def db_table_val_admin(admin_tg_id: int, admin_name: str, admin_username: str, cursor, conn):
    cursor.execute('''INSERT INTO admins
    (admin_tg_id, admin_name, admin_username) 
    VALUES (%s, %s, %s)
    ON CONFLICT (admin_tg_id) 
    DO UPDATE SET 
        admin_name = EXCLUDED.admin_name,
        admin_username = EXCLUDED.admin_username
''', (admin_tg_id, admin_name, admin_username))
    conn.commit()

def db_table_val_app(user_id: int, username:str, question: str, answer: str, status:bool, cursor, conn):
    cursor.execute('''INSERT INTO applications
    (telegram_id, username, question, answer, status) 
    VALUES (%s, %s, %s, %s, %s)
''', (user_id, username, question, answer, status))
    conn.commit()

def if_exist(user_id, cursor):
    cursor.execute('SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = %s)', (user_id,))
    return cursor.fetchone()[0]

def if_admin(user_id, cursor):
    cursor.execute('SELECT EXISTS(SELECT 1 FROM admins WHERE admin_tg_id = %s)', (user_id,))
    return cursor.fetchone()[0]

def if_exist_admin(user_id, cursor):
    cursor.execute('SELECT EXISTS(SELECT 1 FROM admins WHERE admin_tg_id = %s)', (user_id,))
    return cursor.fetchone()[0]