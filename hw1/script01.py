# Name: Jakob Long
# UTEID: Jrl4725

# initializes word list
words = []

# Grabs word file & opens it for reading
with open('/usr/share/dict/words','r') as f:
    words  = f.read().splitlines()
    
words.sort(key=len, reverse=True)

print(words[:5])