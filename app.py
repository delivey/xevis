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

    new_url = generate() # database limit is 10 character
    original_url = request.form.get("url")

    db.execute("INSERT INTO urls (original_url, new_url) VALUES (?, ?)", (original_url, new_url))
    conn.commit()
    return render_template("index.html", new_url=new_url)

@app.route("/<gen>/", methods=["GET"])
def url():
    conn = sqlite3.connect('urls.db') # connects to db
    db = conn.cursor() # creates the cursor for the connection
