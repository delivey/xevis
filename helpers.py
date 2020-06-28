import random
import string
import sqlite3
from urllib.parse import urlparse

def generate():
    conn = sqlite3.connect('urls.db') # connects to db
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
    duplicateString = db.execute("SELECT new_url FROM urls WHERE new_url=(?)", (finalString,))

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