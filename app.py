from flask import Flask, redirect, render_template, request
from helpers import generate, url_validator, generate_qr
import os
import psycopg2

QR_CODE_FOLDER = os.path.join('static', 'qr_codes')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = QR_CODE_FOLDER

@app.route("/")
def index():
    new_url = None
    return render_template("index.html", new_url=new_url)

@app.route("/shorten/", methods=["POST"])
def shorten():
    
    conn = psycopg2.connect( # connects to db
    host="localhost",
    database="urls",
    user="xevis",
    password="xevis")

    db = conn.cursor() # creates the cursor for the connection

    new_url = generate() # database limit is 25 characters
    original_url = request.form.get("url") # gets the url from user input

    qr_id = 'qr_codes/' + str(generate_qr(new_url)) + '.png' # generates the path for the qr code image

    if original_url == "" or not url_validator(original_url):
        return redirect("/") #TODO: make it redirect to error

    try:
        db.execute("SELECT new_url FROM urls WHERE original_url=%s", (original_url, ))
        duplicate_url = db.fetchone()[0]
    except TypeError:
        duplicate_url = False
    
    if duplicate_url != False:
        new_url = duplicate_url
    else:
        db.execute("INSERT INTO urls (original_url, new_url) VALUES (%s, %s)", (original_url, new_url))
        conn.commit()

    return render_template("index.html", new_url=new_url, qr_id=qr_id)

@app.route("/<gen>/", methods=["GET", "POST"])
def url(gen):
    if gen != "/":
        # conn = sqlite3.connect('urls.db') # connects to db
        conn = psycopg2.connect(
        host="localhost",
        database="urls",
        user="xevis",
        password="xevis")

        db = conn.cursor() # creates the cursor for the connection

        try:
            # original_url = db.execute("SELECT original_url FROM urls WHERE new_url=(?)", (gen,)).fetchone()[0]
            db.execute("SELECT original_url FROM urls WHERE new_url=%s", (gen,))
            original_url = db.fetchone()[0]
            return redirect(original_url)
        except TypeError:
            original_url = gen
            return redirect(original_url)
