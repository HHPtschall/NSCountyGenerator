import json


# Opens files and returns usable lists or dictionaries
def open_file(file_name):
    file = open(file_name, 'r')

    if '.txt' in file_name:
        file_output = file.readlines()
    elif '.json' in file_name:
        file_output = json.load(file)
    else:
        file_output = ''

    file.close()

    return file_output


def split_string(initial_string, file):
    if ',' in initial_string:
        temp = initial_string.split(', ')
    else:
        temp = [initial_string]

    output = []
    for i in temp:
        output.append(file[i])
    return output


# Gives the start of the formula based on a list of state inputs
def get_state_string(states):
    if len(states) == 1:
        temp = "{custentity23.custrecord_county_state.id}=" + states[
            0] + ") and ("
    else:
        temp = "{custentity23.custrecord_county_state.id} in ("
        for state in states:
            if state != states[-1]:
                temp += state + ','
            else:
                temp += state

        temp += ") and ("

    return temp


# Initializes necessary variables
state_list = open_file('states.json')
county_list = open_file('input.txt')
counties = []
county_string = ""
FRONT = "UPPER({custentity23.name})=UPPER('"
END = "') or "
DO_NOT_VISIT = ") and ({custentity21.id}='F')"

# Takes out the \n and County in each line
for line in county_list:
    temp = line.strip()
    if ' County' in line:
        temp = temp.replace(' County', '')
    counties.append(temp)

# Creates the meat of the formula by reading in a list and tacking on fronts and backs
for i in counties:
    if i != counties[-1]:
        county_string += FRONT + i + END
    else:
        county_string += FRONT + i + "')"

# Puts together the final formula string
state_input = input("Type in the states you would like to use:\n")
state = get_state_string(split_string(state_input, state_list))
formula_string = state + county_string + DO_NOT_VISIT

# Creates an output text file
output = open("output.txt", 'w')
output.write(formula_string)
output.close()
print('Formula has been generated in the output file to the left')

# TODO Make a ReadMe file to make working with this easier for new people