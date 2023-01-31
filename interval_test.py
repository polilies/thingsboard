import datetime as dt
import time 
secs = [0, 10, 20, 30, 40, 50]

def get_sec():
    return dt.datetime.now().second

while True:
    sec = get_sec()
    if sec in secs:
        print(f"Catch you! The sec is {sec}")
        break
    else:
        print(f"I am on my way! The sec is {sec}")
    time.sleep(1)