Problem Statement: 

Find All Pairs in a List that Sum to a Specific Value
Write a Python function to find all pairs in a list that sum to a specific value.
Input: [1, 2, 3, 4, 5], Sum=6
Output: [(1, 5), (2, 4)]


Solution:

def find_pairs(input_list, specific_sum):
    pairs = []
    seen = set()
    for num in input_list:
        difference = specific_sum - num
        if difference in seen:
            pairs.append((difference, num))
        seen.add(num)
    return pairs

input_list = [1, 2, 3, 4, 5]
specific_sum = 6
print(find_pairs(input_list, specific_sum))

Sample Input: [1, 2, 3, 4, 5]
Expected Output:  [(1, 5), (2, 4)] 
