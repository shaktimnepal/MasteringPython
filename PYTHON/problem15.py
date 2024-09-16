Problem statement:

Group Anagrams Using a Dictionary
Write a Python function to group anagrams from a list of words using a dictionary.

Solution:

def group_anagrams(words):
    anagrams = {}
    for word in words:
        sorted_word = ''.join(sorted(word))
        if sorted_word in anagrams:
            anagrams[sorted_word].append(word)
        else:
            anagrams[sorted_word] = [word]

    return list(anagrams.values())

input_words = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
output = group_anagrams(input_words)
print(output)

Sample Input: ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
Expected Output: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
