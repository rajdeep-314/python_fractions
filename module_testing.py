from frac_testing import frac

x = frac('0.1_6...', '6')
print(x)
print(x.decimal)
print(int(x))
print(float(x))
print(x.numerator, x.denominator, sep = "\t")
print(-x)
print(x**0.5)
print(x/frac(0.25))
print(6*(x + x + x + x + x + x))
print(x + 1)
print(x > frac(1, 37))
print(0.5*x <= 0.1)
print()
print(frac(1, 6) == '0.1_6...')

