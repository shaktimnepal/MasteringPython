Problem Statement:

Reverse a String
Write a Python function to reverse a given string.

Solution:

def string_reverser(given_string):
    return given_string[::-1]

given_string = 'hello'
reversed_string = string_reverser(given_string)
print('Output: ', reversed_string)

Sample Input: "hello"
Expected Output: "olleh"
