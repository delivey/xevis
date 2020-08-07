import qrcode
# import sqlite3
import random
import os
import psycopg2

def generate_id():
    conn = psycopg2.connect(
    host="localhost",
    database="urls",
    user="xevis",
    password="xevis") # connects to db
    db = conn.cursor() # creates the cursor for the connection

    generated_id = random.randint(1, 100000)
    try:
        db.execute("SELECT qr_id FROM qr_codes WHERE qr_id=%s", (generated_id,))
        duplicate = db.fetchone()[0]

        duplicate = True
    except TypeError:
        duplicate = False

    while duplicate == True:
        generated_id = random.randint(1, 100000)
        try:
            db.execute("SELECT qr_id FROM qr_codes WHERE qr_id=%s", (generated_id,))
            duplicate = db.fetchone()[0]
            duplicate = True
        except TypeError:
            duplicate = False

    qr_id = generated_id
    db.execute("INSERT INTO qr_codes (qr_id) VALUES (%s)", (qr_id,))
    conn.commit()
    return qr_id

generate_id()
def generate_qr(url):
    qr_id = generate_id()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    path = f'{os.getcwd()}/static/qr_codes/{qr_id}.png'
    img.save(path)

    return qr_id