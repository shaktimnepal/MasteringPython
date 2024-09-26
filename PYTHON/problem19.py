Problem Statement:

Find Missing Number in an Array
Question: Given a list of integers from 1 to n with one number missing, find the missing number.

Solution:

def find_missing_numbers(arr, n):
    full_set = set(range(1, n + 1))  # Create a set of numbers from 1 to n
    arr_set = set(arr)  # Convert the array to a set
    missing_numbers = list(full_set - arr_set)  # Find the difference between the two sets
    return sorted(missing_numbers)  # Return the missing numbers in sorted order

# Example Usage:
arr = [1, 2,3,4, 5,7,10]  # Missing numbers are 6, 8, 9
n = arr[-1]  # Numbers should be from 1 to last number in array.
print(f"The missing numbers are: {find_missing_numbers(arr, n)}")


Sample Input: [1, 2,3,4, 5,7,10]
Expected Output: The missing numbers are: [6, 8, 9]
