tgClass  = None

def addWords():
    tgClass._callEvent("WordMaster.registerWord", words={
        "startMessage": "Привет! Добро пожаловать в Svint!"
    })

def getWord(name):
    return tgClass._callEvent("WordMaster.getWord", word=name)