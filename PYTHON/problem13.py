Problem statement:

Invert a Dictionary
Write a Python function to invert a dictionary (swap keys and values).

Solution:
def dict_inverter(input):
    inverted_dict = {}
    for x in input:
        y = input[x]
        inverted_dict[y] = x
    return inverted_dict


input = {'a': 1, 'b': 2, 'c': 3}
output = dict_inverter(input)
print(output)

Sample Input: {'a': 1, 'b': 2, 'c': 3}
Expected Output: {1: 'a', 2: 'b', 3: 'c'}


