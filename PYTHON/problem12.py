Problem Statement:

Merge Two Dictionaries
Write a Python function to merge two dictionaries.

Solution:

def merged_dictionary(dict1, dict2):
    dict1_copy = dict1.copy()
    for x,y in dict2.items():
        dict1_copy[x] = y
    return dict1_copy


dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
output = merged_dictionary(dict1, dict2)
print(output)

Sample input: {'a': 1, 'b': 2}, {'b': 3, 'c': 4}
Expected output: {'a': 1, 'b': 3, 'c': 4}
