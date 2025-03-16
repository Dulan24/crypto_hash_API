import psycopg2
import base64

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
    """Create the 'encryption_keys' table in PostgreSQL only if it doesn't exist."""
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        # Check if the table exists before creating it
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'encryption_keys'
            );
        """)
        table_exists = cur.fetchone()[0]

        if not table_exists:
            cur.execute("""
                CREATE TABLE encryption_keys (
                    key_id UUID PRIMARY KEY,
                    key_value TEXT NOT NULL,
                    algorithm TEXT CHECK (algorithm IN ('AES', 'RSA')) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("Table 'encryption_keys' created successfully.")
        else:
            print("Table 'encryption_keys' already exists. Skipping creation.")

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Error creating table: {e}")

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def store_key_in_db(key_id, key_value, algorithm):
    """Store the generated key in the PostgreSQL database."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO encryption_keys (key_id, key_value, algorithm)
        VALUES (%s, %s, %s);
    """, (key_id, key_value, algorithm))

    conn.commit()
    cur.close()
    conn.close()

def get_key_from_db(key_id: str):
    """Retrieves the encryption key from the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT key_value, algorithm FROM encryption_keys WHERE key_id = %s;", (key_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return base64.b64decode(row[0]), row[1]  
    return None, None