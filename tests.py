import psycopg2

conn = psycopg2.connect( # change to your credentials
host="localhost",
database="urls",
user="xevis",
password="xevis")

db = conn.cursor()

db.execute("SELECT * FROM urls")
print(db.fetchall())