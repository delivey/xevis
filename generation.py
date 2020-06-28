import random
import string

def generate():

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
    return finalString