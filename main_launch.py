import threading
import os

def bot_start():
    os.system("python launcher.py")

def web_start():
    os.system("python manage.py runserver")

if __name__ == '__main__':
    t1 = threading.Thread(target=bot_start)
    t2 = threading.Thread(target=web_start)

    t1.start()
    t2.start()





import datetime

def show_time():
    time = datetime.datetime.utcnow()
    print("Hello!")
    print("Current time is: ", time)