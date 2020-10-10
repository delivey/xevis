import random
import string
import qrcode
from urllib.parse import urlparse
import psycopg2
import os

def generate():
    # conn = sqlite3.connect('urls.db') # connects to db
    conn = psycopg2.connect(
    host="localhost",
    database="urls",
    user="xevis",
    password="xevis")

    db = conn.cursor() # creates the cursor for the connection

    letters = random.randint(1, 4)
    digits = random.randint(1, 4) 

    while letters + digits != 6:
        letters = random.randint(1, 4)
        digits = random.randint(1, 4)

    sampleStr = ''.join((random.choice(string.ascii_lowercase) for i in range(letters)))
    sampleStr += ''.join((random.choice(string.digits) for i in range(digits)))
    
    sampleList = list(sampleStr)
    random.shuffle(sampleList)
    finalString = ''.join(sampleList)
    try:
        db.execute("SELECT new_url FROM urls WHERE new_url=%s", (finalString,))
        duplicateString = db.fetchone()[0]
    except TypeError:
        duplicateString = None 

    if finalString == duplicateString:
        generate()
    else: 
        return finalString

def url_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

def generate_qr(url_id):
    
    url = f'http://127.0.0.1:5000/{url_id}'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    path = f'{os.getcwd()}\\static\\qr_codes\\{url_id}.png'
    img.save(path)

    return url_id