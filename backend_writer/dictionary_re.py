import re 

my_dict = dict()

with open(r'x:\path\to\file', 'r') as data:
    for line in data:
        match = re.search(pattern, line)
        if match:
            one_tuple = match.group(3, 2)
            my_dict[one_tuple[0]] = one_tuple[1]
