Problem Statement:

Compress a String Using the Counts of Repeated Characters 
Write a Python function to perform basic string compression using the counts of repeated characters.
Input: "aabcccccaaa"
Output: "a2b1c5a3"

Solution:

def compress_string(s):
    compressed = ''
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            compressed += s[i - 1] + str(count)
            count = 1

    compressed += s[-1] + str(count)
    return compressed if len(compressed) < len(s) else s

input_string = "aabcccccaaa"
output = compress_string(input_string)
print(output)

Sample Input: "aabcccccaaa"
Expected Output: "a2b1c5a3"
