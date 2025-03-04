import os

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'tgbot_vc')
DB_USER = os.getenv('DB_USER', 'egor')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'wA0rF-rD6Gx4')
DB_PORT = int(os.getenv('DB_PORT', 5432))
