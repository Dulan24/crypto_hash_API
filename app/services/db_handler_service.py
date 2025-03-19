import psycopg2
import base64
from app.config import DataBase_HOST, DataBase_NAME, DataBase_PASSWORD, DataBase_PORT, DataBase_USER

# Database Credentials
DB_NAME = DataBase_NAME
DB_USER = DataBase_USER
DB_PASSWORD = DataBase_PASSWORD
DB_HOST = DataBase_HOST
DB_PORT = DataBase_PORT

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
                    private_key TEXT,  -- Base64 encoded private key (for RSA only)
                    public_key TEXT,   -- Base64 encoded public key (for RSA)
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


def get_private_key_from_db(key_id: str):
    """Retrieves the encryption key from the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT private_key, algorithm FROM encryption_keys WHERE key_id = %s;", (key_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return base64.b64decode(row[0]), row[1]  
    return None, None

def get_public_key_from_db(key_id: str):
    """Retrieves the encryption key from the database."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT public_key, algorithm FROM encryption_keys WHERE key_id = %s;", (key_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return base64.b64decode(row[0]), row[1]  
    return None, None


def store_rsa_keys_in_db(key_id, private_key, public_key):
    """Stores RSA private and public keys in the PostgreSQL database."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO encryption_keys (key_id, private_key, public_key, algorithm)
        VALUES (%s, %s, %s, 'RSA')
        ON CONFLICT (key_id) DO UPDATE 
        SET private_key = EXCLUDED.private_key, 
            public_key = EXCLUDED.public_key;
    """, (key_id, private_key, public_key))

    conn.commit()
    cur.close()
    conn.close()

def store_aes_key_in_db(key_id, aes_key):
    """Stores the AES encryption key in the database."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO encryption_keys (key_id, private_key, algorithm)
        VALUES (%s, %s, 'AES')
        ON CONFLICT (key_id) DO UPDATE 
        SET private_key = EXCLUDED.private_key;
    """, (key_id, aes_key))

    conn.commit()
    cur.close()
    conn.close()
