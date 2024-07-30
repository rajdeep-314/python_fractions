from frac import *
import os
import platform

command = {'Linux': 'clear',
           'Windows': 'cls'}

def clear(text = ''):
    print()
    input("Hit ENTER to continue")
    print()
    os.system(command.get(platform.system(), ''))
    print(text, end = '')

# Same ID
print("> Instance space demo\n")
frac1 = frac(1, 2)
frac2 = frac(10, 20)
print("id(frac1)\t-->", id(frac1), sep = "\t")
print("id(frac2)\t-->", id(frac2), sep = "\t")
print("frac1 is frac2\t-->", frac1 is frac2, sep = "\t")

clear()

# 3*0.1 = 0.3
print("> 3*0.1 = 0.3\n")
print("3*frac(0.1) =", 3*frac(0.1), "=", float(3*frac(0.1)))

clear()

# pi
print("> Pi summation\n")

print("Processing...")
my_pi = 0
for i in range(10000):
    my_pi += frac((-1)**i, 2*i+1)

my_pi *= 4

print("Decimal representation:", my_pi.decimal)
print()
print("Floating point representation:", float(my_pi))

clear()

# Geometric sum
print("> Geometric sum\n")

current_sum = 0
for i in range(1, 1001):
    current_sum += frac(1, 2**i)

print("Decimal representation:", current_sum.decimal)
print()
print("Floating point representation:", float(current_sum))

clear("End of demo\n")
