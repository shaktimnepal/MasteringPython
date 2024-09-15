Problem statement:

Find Key with Maximum Value
Write a Python function to find the key with the maximum value in a dictionary.

Solution:

def key_with_max_value(input):
    max_value = 0
    for x,y in input.items():
        if y > max_value:
            max_value = y
            max_key = x
    return max_key

input = {'a': 10, 'b': 20, 'c': 5}
output = key_with_max_value(input)
print(output)

Sample Input: {'a': 10, 'b': 20, 'c': 5}
Expected Output: 'b'
