 #Use of try and except problem

sh = input('Enter Hours:') #Enter no. of hours worked
sr = input('Enter rate:') #Enter rate of pay per hour
try:
    fh = float(sh) #changes hour type into float
    fr = float(sr) #changes rate type into float
except:
    print('Error, please enter a numeric input')
    quit()
if fh > 40:
    xp = 40 * fr + (fh - 40) * 1.5 * fr #calculates total pay that is regular pay plus over time pay
else:
    xp = fh * fr #calculates only the regular pay
print('Pay:', xp) # prints back the total Pay
