Problem statement:

Find the Intersection of Two Lists
Write a Python function to find the intersection of two lists.

Solution:

def find_intersection(list1, list2):
    intersection_list = []
    for x in list1:
        if x in list2:
            intersection_list.append(x)
    return intersection_list

list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
final_list = find_intersection(list1, list2)
print(final_list)

Sample Input: [1, 2, 3, 4], [3, 4, 5, 6]

Expected Output: [3, 4]
