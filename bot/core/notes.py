"""
Oracle note saving script
"""

import os

def new(filename, text):
    if os.path.exists('../bot/notes/' + filename + '.txt'):
        return False
    else:
        f = file('../bot/notes/' + filename + '.txt', 'w')
        f.write(text)
        f.close()
        return True

def listall():
    return os.listdir('../bot/notes/')

def find(term):
    tlist = list()
    results = []
    for line in tlist:
        if term in line:
            results.append(line)
    return results

def delete(filename):
    if os.path.exists('../bot/notes/' + filename + '.txt'):
        os.remove('../bot/notes/' + filename + '.txt')
        return True
    else:
        return False

def edit(filename, text):
    if not os.path.exists('../bot/notes/' + filename + '.txt'):
        return False
    else:
        f = file('../bot/notes/' + filename + '.txt', 'w')
        f.write(text)
        f.close()
        return True
        
def get(filename):
    if not os.path.exists('../bot/notes/' + filename + '.txt'):
        return "File not found"
    else:
        with open('../bot/notes/' + filename + '.txt','r') as f:
            text = f.read()
        return text