# Name: Jakob Long
# UTEID: Jrl4725
import names

# Iterates 5 times to get the required 5 names
for i in range(5):
    # Initializes name, to the first name generated
    name = names.get_full_name()
    
    # Ensures the name is only 8 characters, plus one character for the space
    while len(name) != 9:
        name = names.get_full_name()
    
    print(name)