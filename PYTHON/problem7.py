Problem statement:

Write a Python function that counts the frequency of each word in a given paragraph. 
The function should return the result as a dictionary. 
Additionally, provide a way to retrieve the most frequently occurring word(s) from this dictionary


Solution:

def count_word_frequency(paragraph):
    paragraph = paragraph.lower()

    words = paragraph.split()
    word_count = {}

    for word in words:
        if word in word_count:
            word_count[word] =  word_count[word] + 1
        else:
            word_count[word] = 1

    return word_count

def find_most_frequent_words(word_count):
    max_count = max(word_count.values())

    most_frequent_words = [word for word, count in word_count.items() if count == max_count]

    return most_frequent_words, max_count

input_paragraph = "Hello world Hello world This world is full of surprises Surprises are everywhere; surprises are fun"

word_count = count_word_frequency(input_paragraph)
print(word_count)

most_frequent_words, max_count = find_most_frequent_words(word_count)
print("Most Frequent word(s):", most_frequent_words)


Sample Input: 
"Hello world Hello world This world is full of surprises Surprises are everywhere; surprises are fun"

Expected Output: 
{'hello': 2, 'world': 3, 'this': 1, 'is': 1, 'full': 1, 'of': 1, 'surprises': 3, 'are': 2, 'everywhere;': 1, 'fun': 1}
Most Frequent word(s): ['world', 'surprises']
