import psycopg2

conn = psycopg2.connect( # change to your credentials
host="localhost",
database="urls",
user="xevis",
password="xevis")

db = conn.cursor() # creates a cursor for the connection

db.execute("DROP TABLE IF EXISTS urls") # drops the 'urls' table if it already exists
db.execute( # creates the 'urls' table
"""
CREATE TABLE urls (
    original_url VARCHAR(255) NOT NULL,
    new_url VARCHAR(25) NOT NULL
)
"""
)
print("'urls' table created successfully!")

db.execute("DROP TABLE IF EXISTS qr_codes")
db.execute(
    """
    CREATE TABLE qr_codes (
    qr_id INTEGER NOT NULL
    )
    """
)
print("'qr_codes' table created successfully!")
conn.commit() # commits the created data

db.execute("INSERT INTO urls (original_url, new_url) VALUES (%s, %s)", ('test successful', 'DB creation successful!'))
db.execute("SELECT new_url FROM urls WHERE original_url=%s", ('test successful',))
successful = db.fetchone()[0]
if successful == 'DB creation successful!':
    print('Database creation successful and tested!')

db.execute("DELETE FROM urls WHERE new_url=%s", ('test successful',))

conn.commit()
conn.close()