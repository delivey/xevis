from flask import Flask, redirect, render_template, request
import sqlite3
from generation import generate

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    gen = generate()
    return redirect("/")
