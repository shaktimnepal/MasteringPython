#print largest number in a list

numbers = [1,2,3,4,5,6,7,8,9,10]
z = numbers[0]
for x in numbers:
    if z<x:
        z = x
print(z)
