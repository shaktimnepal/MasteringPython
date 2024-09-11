Problem statement:
Write a Python function to remove duplicates from a list while preserving the order.

Solution:

def remove_duplicates(input_list):
    unique_list = []
    for x in input_list:
        if x not in unique_list:
            unique_list.append(x)

    return unique_list

input_list = [1, 2, 2, 3, 4, 4, 5]
new_list = remove_duplicates(input_list)
print(new_list)

Sample Input:[1, 2, 2, 3, 4, 4, 5]
Expected Output: [1, 2, 3, 4, 5] 
