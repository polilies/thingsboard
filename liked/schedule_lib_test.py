#https://schedule.readthedocs.io/en/stable/
import schedule
import time

def trace():
    print("it works")
    
schedule.every().minute.at(":55").do(trace)    
    
while True:
    schedule.run_pending()
    time.sleep(1)
    
    