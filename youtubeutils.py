import re

def string2filename(string):
    string = string.strip().replace('[', '(').replace(']', ')').replace(':', ' -')
    return re.sub(r'(?u)[^-\w.() ]', '', string)
 
def capitalized_case(s):
    s = s.strip()
    return " ".join(w.capitalize() for w in s.split())

def stringify_index(index):
    if index < 10:
        return '0' + str(index)
    return str(index)

