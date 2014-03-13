import os

import connect as c

# Check whether nick has mail in /mail/
def check(nick):
    letters = []
    for f in os.listdir('mail/'):
        text = f.split(" ")
        if nick in text:
            mail = f.split(nick + " - ")[1].split(".txt")[0]
            letters.append(mail)
    return letters

# Message mail to the user
def read(nick, title):
    if os.path.exists('mail/' + nick + ' - ' + title + '.txt'):
        with open('mail/' + nick + ' - ' + title + '.txt','r') as f:
            lines = f.read()
            lines = lines.split('\n')
            return (lines[1] + " says: " + lines[0])
            f.close()
    return "No mail under that name"

# Create a new mail
def send(nick, recipient, title, msg):
    if os.path.exists('mail/' + recipient + ' - ' + title + '.txt'):
        return False
    else:
        with open('mail/' + recipient + ' - ' + title + '.txt','w') as f:
            f.write(str(msg) + '\n' + nick)
            f.close()
        return True

# Delete mail (no way to delete other's mail currently)
def delete(nick, title):
    if os.path.exists('mail/' + nick + ' - ' + title + '.txt'):
        os.remove('mail/' + nick + ' - ' + title + '.txt')
        return True
    return False
