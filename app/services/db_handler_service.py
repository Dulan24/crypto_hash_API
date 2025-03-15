import psycopg2

# Database Credentials
DB_NAME = "key_db"
DB_USER = "postgres"
DB_PASSWORD = "1234phs"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_database():
    """Create the PostgreSQL database if it doesn't exist."""
    try:
        conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        conn.autocommit = True  # Required for CREATE DATABASE
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f" Error creating database: {e}")

def create_table():
    """Create the 'encryption_keys' table in PostgreSQL."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS encryption_keys (
                key_id UUID PRIMARY KEY,
                key_value TEXT NOT NULL,
                algorithm TEXT CHECK (algorithm IN ('AES', 'RSA')) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("Table 'encryption_keys' created successfully.")

    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
