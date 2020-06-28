from flask import Flask, redirect, render_template, request
import sqlite3
from generation import generate

app = Flask(__name__)

@app.route("/")
def index():
    new_url = None
    return render_template("index.html", new_url=new_url)

@app.route("/shorten", methods=["POST"])
def shorten():

    conn = sqlite3.connect('urls.db') # connects to db
    db = conn.cursor() # creates the cursor for the connection

    new_url = generate() # database limit is 20 character
    original_url = request.form.get("url")

    db.execute("INSERT INTO urls (original_url, new_url) VALUES (?, ?)", (original_url, new_url))
    conn.commit()
    return render_template("index.html", new_url=new_url)

@app.route("/<gen>/", methods=["GET", "POST"])
def url(gen):
    if gen != "" or "/shorten":
        conn = sqlite3.connect('urls.db') # connects to db
        db = conn.cursor() # creates the cursor for the connection

        original_url = db.execute("SELECT original_url FROM urls WHERE new_url=(?)", (gen,)).fetchone()[0]
        return redirect(original_url)
