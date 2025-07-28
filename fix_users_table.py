import psycopg2
from config.settings import DB_CONFIG

def drop_users_table():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users;")
        conn.commit()
        print("✓ Dropped old 'users' table successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        print("✗ Error dropping 'users' table:", e)

if __name__ == "__main__":
    drop_users_table() 