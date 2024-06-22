# I explored a few things with __setattr__ here but
# scrapped the idea later as it wasn't really practical
# In this version, everytime the numerator and denominator
# attributes are "manually" changed using self.numerator = new_numerator,
# for example, they're reduced to the simplest form before assignment

# I liked my implementation of this, so I decided to keep the program
# as an artifact. I will probably (definitely) remove this in the final version

# A class to implement fractions

import math
import re

# Custom exception class
class FractionError(Exception):
    pass

class frac:
    '''Fractions

Constructor:
    frac()                  ->     0 by 0
    frac(int a)             ->     a by 1
    frac(int a, int b)      ->     a by b
    frac(float a)           ->     fractional representation of a (Ex : 2.2 -> 22 by 10)
    frac(float a, float b)  ->     fractional representation of a/b

    Similarly, either of the arguments (or both) can be a 'frac' object as well'''


    # To obtain the number of repeating digits in 1/n, and the number of places before them
    # Ex: decimal_helper(6) = (1, 1) as after 1 decimal place, 1 digit repeats infinitely in 0.1666...
    # Output format : Tuple -> (a, b) where after 'a' decimal places, 'b' digits repeat
    @staticmethod
    def decimal_helper(n):
        counter_two = 0         # Number of two's in the prime-factorization of n
        counter_five = 0        # Number of five's in the prime-factorization of n
        
        while n%2 == 0:
            n //= 2
            counter_two += 1
        while n%5 == 0:
            n //= 5
            counter_five += 1

        # max(counter_two, counter_five) gives how many times we must
        # multiply 1/n by 10 till the denominator isn't a multiple of
        # 2 or 5. This is the number of decimal places after which the
        # repetition begins, if it does.
        pre_repetition = max(counter_two, counter_five)

        # 'n' is not a multiple of 2 or 5 now
        # For such an n != 1, we can evaluate the number of digits that
        # repeat in it's decimal expansion as follows :
        # We take a number 'm' from 1 to n-1 and stop at the first value
        # of 'm' such that (10**m mod n) == 1
        for i in range(1, n):
            if 10**i % n == 1:
                return (pre_repetition, i)
        
        # For cases where the initial 'n' is of the form 2**p * 5**q for p, q >= 0
        # In which case, there is no repetition and the decimal expansion is simply
        # 'pre_repetition' number of digits, followed by infinite leading zeroskjk
        return (pre_repetition, 0)
    
    @staticmethod
    def simplification_helper(a, b):            # Reduces a/b to it's simplest form and returns (a, b) as a tuple
        gcd_ = math.gcd(a, b)
        return (a//gcd_, b//gcd_)

    # Managing attribute changes (and initializations)
    def __setattr__(self, attribute_name, value):
        flag = False
        # If either of 'numerator' or 'denominator' was re-assigned (needs re-simplification)
        if attribute_name in ['numerator', 'denominator'] and attribute_name in self.__dict__:
            flag = True

        super().__setattr__(attribute_name, value)

        if flag:
            # Modifying the numerator and denominator before re-assigning their corresponding attributes
            new_numerator, new_denominator = self.simplification_helper(self.numerator, self.denominator)
            super().__setattr__('numerator', new_numerator)
            super().__setattr__('denominator', new_denominator)

    # Initialization, with exception handling
    def __init__(self, a=0, b=1):
        if b == 0:
            raise FractionError("Denominator can't be zero")

        if not (isinstance(a, (int, float, frac)) and isinstance(b, (int, float, frac))):
            raise FractionError("Invalid arguments passed - Only 'int', 'float' and 'frac' objects are accepted")

        elif isinstance(a, float):
            if isinstance(b, int):
                float_parts = str(a).split(".")
                a = int("".join(float_parts))
                b = 10**len(float_parts[1])
            elif isinstance(b, (float, frac)):
                f1 = frac(a)
                f2 = frac(b)
                f_ = f1 * f2.reciprocal()
                a, b = f_.numerator, f_.denominator
        elif isinstance(a, int) and isinstance(b, (float, frac)):
            f_ = frac(b)
            a *= f_.denominator
            b = f_.numerator
        elif isinstance(a, frac):
            f1 = a
            f2 = frac(b)
            a = f1.numerator*f2.denominator
            b = f1.denominator*f2.numerator

        if b < 0:               # Managing signs
            a *= -1
            b *= -1

        simplified = self.simplification_helper(a, b)          # Reduced to co-primes
        self.numerator, self.denominator = simplified

    def reciprocal(self):           # Returns the reciprocal of the instance, if it exists (denominator != 0)
        return frac(self.denominator, self.numerator)

    # Returns the decimal representation of the fraction as a string
    # Examples:
    # 4/2    -->   2.0
    # 1/5    -->   0.2
    # 1/6    -->   0.1_6...             (to denote 0.1666...)
    # 1/3    -->   0.3...
    # 22/7   -->   3.142857...
    # 22/700 -->   0.03_142857...       (to denote 0.03142857142857... or 0.03(142857)...)
    def decimal(self):
        a = self.numerator
        b = self.denominator

        pre_decimal_string = str(a // b) + "."
        a %= b

        if a == 0:      # If 'b' completely divides 'a'
            return pre_decimal_string + "0"

        places, digits = self.decimal_helper(b)
        n = a * 10**places              # To evaluate the non-repeating part
        non_repeating_string = ""
        if places:                      # If there is a non-repeating part
            non_repeating_string = str(n // b).zfill(places) + "_"
        if digits:                      # If there is a repeating part
            repeating_string = str(((n % b) * 10**digits) // b).zfill(digits)
            return pre_decimal_string + non_repeating_string + repeating_string + "..."

        return pre_decimal_string + non_repeating_string[:-1]
    
    def __repr__(self):
        return "Fraction: " + str(self.numerator) + " by " + str(self.denominator)

    @staticmethod
    def try_conversion(other):      # Attempts to convert 'other' to a 'frac' object with a try...except clause
        try:
            return frac(other)
        except FractionError:
            raise TypeError(f"{type(other)} object can't be interpreted as a 'frac' object")

    def __eq__(self, other):        # Implements a == b 
        other = self.try_conversion(other)
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __lt__(self, other):        # Implements a < b
        other = self.try_conversion(other)
        return self.numerator*other.denominator < other.numerator*self.denominator

    def __lte__(self, other):       # Implements a <= b
        return self < other or self == other

    def __gt__(self, other):        # Implements a > b
        other = self.try_conversion(other)
        return self.numerator*other.denominator > other.numerator*self.denominator

    def __gte__(self, other):       # Implements a >= b
        return self > other or self == other

    def __ne__(self, other):        # Implements a != b
        return not self == other

    def __add__(self, other):       # Implements a + b
        other = self.try_conversion(other)
        return frac(self.numerator*other.denominator + self.denominator*other.numerator, self.denominator*other.denominator)

    def __mul__(self, other):       # Implements a * b
        other = self.try_conversion(other)
        return frac(self.numerator*other.numerator, self.denominator*other.denominator)

    def __radd__(self, other):      # Implements b + a
        return self + other
    
    def __rmul__(self, other):      # Implements b * a
        return self * other

    def __int__(self):              # Implements int(a)
        return self.numerator // self.denominator

    def __float__(self):            # Implements float(a)
        # Passes at least 16 decimal places to the float function, and
        # at least one cycle of the repeating digits, if they exist
        decimal_string = self.decimal()
        if decimal_string[-1] != ".":
            return float(decimal_string)

        exp = re.compile(r'\.|_')
        parts = exp.split(decimal_string[:-3])

        if len(parts) == 2:
            repeating = len(parts[1])
            return float(parts[0] + "." + parts[1]*math.ceil(16/repeating))
        else:
            non_repeating = len(parts[1])
            repeating = len(parts[2])
            repeating_cycles = math.ceil((16 - non_repeating) / repeating)
            if repeating_cycles == 0:
                repeating_cycles = 1
            return float(parts[0] + "." + parts[1] + parts[2]*repeating_cycles)
 
    def __truediv__(self, other):       # Implements a / b
        other = self.try_conversion(other)
        return self * other.reciprocal()

    def __rtruediv__(self, other):      # Implements b / a
        other = self.try_conversion(other)
        return other / self
    
    def __neg__(self):      # Implements -a
        return frac(-self.numerator, self.denominator)

    def __pow__(self, other):       # Implements a**b
        return frac(self.numerator ** other, self.denominator ** other)

    def __invert__(self):      # Implement ~a to obtain the decimal representation of 'a'
        return self.decimal()

x = frac(1, 5)
print(x, ~x, sep = "\t\t")
x.numerator = 10
print(x, ~x, sep = "\t\t")
x.denominator = 2
print(x, ~x, sep = "\t\t")

