# Name: Jakob Long
# UTEID: Jrl4725
import names
name_list = []

# Define the function to determine the length of a name
def name_length(name):
    # Removes the spaces from the names generated & gets the length
    return len(name.replace(" ", ""))

# Generate a list of five different full names
for i in range(5):
    name_list.append(names.get_full_name())

# Print each name followed by the length of the name
for name in name_list:
    print(name, name_length(name))