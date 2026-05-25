import pandas as pd
from sqlalchemy import create_engine, text

# 1. Define your connection variables
DB_USER = "postgres"
DB_PASSWORD = "Postgres" 
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "bank_reviews"

# 2. Create the connection URL string
# Format: postgresql://username:password@host:port/database_name
connection_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("🔄 Connecting to the PostgreSQL database...")
engine = create_engine(connection_url)

# 3. Write raw SQL code to create tables as a multi-line string
create_tables_sql = """
-- Create the Banks parent table first
CREATE TABLE IF NOT EXISTS banks (
    bank_id VARCHAR(50) PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(100) NOT NULL
);

-- Create the Reviews child table second (because it references the banks table)
CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(100) PRIMARY KEY,
    bank_id VARCHAR(50) REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL,
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(20) NOT NULL,
    sentiment_score NUMERIC(5, 4) NOT NULL,
    identified_theme VARCHAR(50) NOT NULL,
    source VARCHAR(50) DEFAULT 'Google Play Store'
);
"""

# 4. Execute the SQL command using Python
try:
    with engine.begin() as connection:
        # Wrap our SQL string inside SQLAlchemy's text function
        connection.execute(text(create_tables_sql))
    print("✅ Success! Tables 'banks' and 'reviews' have been created inside PostgreSQL.")
except Exception as e:
    print(f"❌ An error occurred while creating tables: {e}")


# 4. Execute the SQL command and IMMEDIATELY double-check it
try:
    with engine.begin() as connection:
        print("🛠️ Sending table creation commands to PostgreSQL...")
        connection.execute(text(create_tables_sql))
        print("✅ SQL code executed.")
        
        # ACTIVE VERIFICATION: Ask the database right now if the tables exist
        print("🔍 Asking database to list its active tables...")
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """))
        
        tables = [row[0] for row in result]
        print(f"📦 Tables actually found inside this database: {tables}")

except Exception as e:
    print(f"❌ An error occurred while creating tables: {e}")