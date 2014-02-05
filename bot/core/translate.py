import connect as c

typo = [
    ]
    
translation = [
    ["i gotta","I have to"],
    ["gotta","have to"],
    ["thar","there"],
    ["heya","hey"],
    ["heyo","hey"],
    ["hola","hello"],
    [" ola"," hello"],
    [" ello"," hello"],
    ["yo","hello"],
    ["aussie","Australian"],
    ["gonna","going to"],
    ["brb","be right back"],
    ["bbl","be back later"],
    ["bbs","be back soon"],
    ["ttyl","talk to you later"],
    ["omw","on my way"],
    ["wanna","want to"],
    ["yep","yes"],
    ["ye ","yes"],
    ["yup","yes"],
    ["nop","nope"],
    ["t\"was","it was"],
    ["soz","sorry"],
    ["u","you"],
    ["ur","your/you\"re"],
    ["dropd","dropped"],
    ["wut","what"],
    ["wat","what"],
    ["dat","that"]
    ]
    
def requires_translate(message):
    words = message.split(" ")
    for w in words:
        for t in translation:
            if w == t[0]:
                return True
                break
    return False
    
def translate_result(message):
    for lost in translation:
        message = message.replace(lost[0],lost[1])
    return message
    
def autocorrect_result(message):
    for error in typo:
        message = message.replace(error[0],error[1])
    return message
    