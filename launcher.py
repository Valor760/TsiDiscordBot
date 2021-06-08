from lib.bot import bot
import os
import threading

def django_start():
    os.system("python manage.py runserver")

t1 = threading.Thread(target=django_start)
t1.start()


bot.run()