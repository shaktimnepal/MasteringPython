Problem Statement:

Count Vowels in a String
Question: Write a Python function to count the number of vowels (a, e, i, o, u) in a given string.
Input: "Hello World"
Output: 3

Solution:

def vowels_counter(given_string):
    vowels = list(['a','e','i','o','u'])
    z = 0
    for x in given_string:
        if x in vowels:
            z = z+1

    return z

given_string = 'Hello World'
vowel_numbers = vowels_counter(given_string)
print('Output: ', vowel_numbers)


Sample Input: "Hello World"
Expected Output: 3
