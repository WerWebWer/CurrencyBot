
from datetime import datetime

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def log(msg, text):
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' | ' + str(msg.chat.id) + ' | ' +
        str(msg.from_user.username) + ' - ' + str(msg.from_user.first_name) + ' ' + str(msg.from_user.last_name) + ' | ' + 
        str(text))

def log_bot(msg, text):
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' | ' + str(msg.chat.id) + ' | BOT | ' + 
        str(text))

def log_for_buttons(id, call, text):
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' | ' + str(id) + ' | ' +
        str(call.from_user.username) + ' - ' + str(call.from_user.first_name) + ' ' + str(call.from_user.last_name) + ' | ' + 
        str(text))
