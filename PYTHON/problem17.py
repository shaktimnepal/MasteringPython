Problem Statement:

6. Find the First Non-Repeating Character
Write a Python function to find the first non-repeating character in a given string and return its index.

Solution:

input_string = "swissabaawc"
char_count = {}

for i in range(len(input_string)):
    char = input_string[i]
    if char not in char_count:
        char_count[char] = 1
    else:
        char_count[char] = char_count[char] + 1

for i in range(len(input_string)):
    char = input_string[i]
    if char_count[char] == 1:
        print(i)
        break

Sample Input: "swissabaawc"
Expected Output: 2 (for 'i' in "swissabaawc")
