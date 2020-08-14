import qrcode
# import sqlite3
import random
import os
import psycopg2

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

    path = f'{os.getcwd()}/static/qr_codes/{url_id}.png'
    img.save(path)

    return url_id