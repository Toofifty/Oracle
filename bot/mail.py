"""
Oracle - Mail Handler
"""

import connect as c
import os

def check(nick):
    letters = []
    for file in os.listdir('../bot/mail/'):
        text = file.split(" ")
        if nick in text:
            mail = file.split(nick + " - ")[1].split(".txt")[0]
            letters.append(mail)
    return letters
            

def read(nick, title):
    if os.path.exists('../bot/mail/' + nick + ' - ' + title + '.txt'):
        with open('../bot/mail/' + nick + ' - ' + title + '.txt','r') as f:
            lines = f.read()
            lines = lines.split('\n')
            return (lines[1] + " says: " + lines[0])
            f.close()
    return "No mail under that name"

def send(nick, recipient, title, msg):
    if os.path.exists('../bot/mail/' + recipient + ' - ' + title + '.txt'):
        return False
    else:
        with open('../bot/mail/' + recipient + ' - ' + title + '.txt','w') as f:
            f.write(str(msg) + '\n' + nick)
            f.close()
        return True

def delete(nick, title):
    if os.path.exists('../bot/mail/' + nick + ' - ' + title + '.txt'):
        os.remove('../bot/mail/' + nick + ' - ' + title + '.txt')
        return True
    return False