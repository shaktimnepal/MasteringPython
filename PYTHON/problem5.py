#Pay computation Using Function

def computepay(hours, rate):
    if hours > 40:
        pay = 40 * fr + (fh - 40) * 1.5* fr
    else:
        pay = hours * rate
    return pay
sh = input('Enter Hours:') #Enter no. of hours worked
sr = input('Enter rate:') #Enter rate of pay per hour
fh = float(sh) #changes hour type into float
fr = float(sr) #changes rate type into float

pay = computepay(fh,fr)

print('Pay is', pay)
