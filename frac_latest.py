# New in this version :
# 1. Fractions with equivalent numerators and denominators share the same memory address for efficiency
# 2. Support for an optional negative sign for string inputs

# A class to implement fractions

import math
import re

# Custom exception class
class FractionError(Exception):
    pass

class frac:
    '''Fractions

Constructor:
    frac()               -->       0 by 0
    frac(int a)          -->       a by 1
    frac(float a)        -->       fractional representation of 'a' (Ex: 2.2 -> 22 by 10)
    frac(string a)       -->       fractional representation of 'a' (Ex: '2/3' -> 2 by 3, '0.3...' -> 1 by 3, '0.1_6...' -> 1 by 6)
    frac(frac a)         -->       a.numerator by a.denominator

    If two arguments are passed, say a and b, then the resulting fraction is equivalent to frac(a) by frac(b)

    Example:
        You can define 2/3 with the following calls (among others):
            frac(2, 3)
            frac('2/3')
            frac('-2/3', -1)
            frac('2/3', 1.0)
            frac('2/3', '1')
            frac('0.6...')
            frac('0.6...', 1)
            frac('0.6...', '1.0')
            frac('-0.6...', '1/-1')'''

    # Note : _instance_space might cause problems with inheritence
    _instance_space = {}
    _latest_a = 0
    _latest_b = 0

    # Regular expressions for string input during initialization
    # Type 1 : num/num         -->   1/2, -20/300, 40/-50, -20/-3
    # Type 2 : num.num         -->   4, -5, 4.25, -3.2, 4.0
    # Type 3 : num.num...      -->   4.34..., -0.3...
    # Type 4 : num.num_num...  -->   4.3_4..., -0.1_6...
    _t1 = re.compile(r'-{0,1}\d+/-{0,1}\d+')
    _t2_1 = re.compile(r'-{0,1}\d+')              # No decimal point
    _t2_2 = re.compile(r'-{0,1}\d+\.\d+')         # With a decimal point
    _t3 = re.compile(r'-{0,1}\d+\.\d+\.{3}')
    _t4 = re.compile(r'-{0,1}\d+\.\d+_\d+\.{3}')

    max_repeating_digits = 2000             # Max repeating digits allowed

    @staticmethod
    def _expression_match(string, expr):         # Returns if the string in it's entirety matches expr
        for match in expr.finditer(string):
            if match[0] == string:
                return True
        return False

    # To obtain the number of repeating digits in 1/n, and the number of places before them
    # Ex: _decimal_helper(6) = (1, 1) as after 1 decimal place, 1 digit repeats infinitely in 0.1666...
    # Output format : Tuple -> (a, b) where after 'a' decimal places, 'b' digits repeat
    @staticmethod
    def _decimal_helper(n):
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

            # To prevent it from taking a long long time
            if i == frac.max_repeating_digits:
                print("Warning: Repeating digits truncated to", frac.max_repeating_digits)
                print("Use frac.max_repeating_digits to change")
                return (pre_repetition, frac.max_repeating_digits)
        
        # For cases where the initial 'n' is of the form 2**p * 5**q for p, q >= 0
        # In which case, there is no repetition and the decimal expansion is simply
        # 'pre_repetition' number of digits, followed by infinite leading zeroskjk
        return (pre_repetition, 0)
    
    # Creating a new instance or returning a pre-existing one from instance_space
    def __new__(cls, a=0, b=1):
        # Invalid argument type
        if not (isinstance(a, (int, float, str, frac)) and isinstance(b, (int, float, str, frac))):
            raise FractionError("Invalid arguments passed - Only 'int', 'float', 'str' and 'frac' objects are accepted")

        if isinstance(a, int):
            a_ = a
            b_ = 1
        elif isinstance(a, float):
            float_parts = str(a).split(".")
            a_ = int("".join(float_parts))
            b_ = 10**len(float_parts[1])
        elif isinstance(a, str):
            if cls._expression_match(a, cls._t1):
                a_, b_ = [int(i) for i in a.split('/')]
            elif cls._expression_match(a, cls._t2_1) or cls._expression_match(a, cls._t2_2):
                portions = a.split(".")
                sign = 1 - 2*(portions[0][0] == '-')
                a_ = abs(int(portions[0]))
                if len(portions) == 1:
                    b_ = 1
                else:
                    post_decimal = portions[1]
                    b_ = 10**len(post_decimal)
                    a_ = a_*b_ + int(post_decimal)
                a_ *= sign
            elif cls._expression_match(a, cls._t3):
                portions = [i for i in a.split(".") if i]
                b_ = 10**len(portions[1]) - 1
                a_ = (1 - 2*(portions[0][0] == '-'))*(abs(int(portions[0]))*b_ + int(portions[1]))
            elif cls._expression_match(a, cls._t4):
                portions = [i for i in a.split(".") if i]
                sign = 1 - 2*(portions[0][0] == '-')
                pre_decimal = abs(int(portions[0]))
                post_decimal_1, post_decimal_2 = portions[1].split("_")
                l1 = len(post_decimal_1)
                l2 = len(post_decimal_2)
                post_decimal_1, post_decimal_2 = int(post_decimal_1), int(post_decimal_2)
                b_ = 10**l1 * (10**l2 - 1)
                a_ = pre_decimal*b_ + post_decimal_1*(b_ // 10**l1) + post_decimal_2
                a_ *= sign

            else:
                raise FractionError("Invalid string input format")
        else:
            a_ = a.numerator
            b_ = a.denominator

        # Exception for denominator being zero
        if b_ == 0:
            raise FractionError("Denominator can't be zero")

        # Base case for initialization
        if isinstance(b, int):
            a = a_
            b *= b_
        else:
            f2 = frac(b)
            a = a_ * f2.denominator
            b = b_ * f2.numerator

        if b < 0:               # Managing signs
            a *= -1
            b *= -1

        # Reducing to co-primes
        gcd_ = math.gcd(a, b)
        a //= gcd_
        b //= gcd_
        cls._latest_a = a
        cls._latest_b = b
        
        return cls._instance_space.get((a, b), super().__new__(cls))

    # Initialization, with exception handling
    def __init__(self, *args):
        a = self._latest_a
        b = self._latest_b
        if (a, b) not in self._instance_space:
            self._instance_space[(a, b)] = self
            self._numerator = a
            self._denominator = b

            # All these attributes are evaluated during the first call to them
            # and are then stored to make subsequent use of their corresponding
            # methods faster
            # Fractions are meant to be immutable, so after the numerator and
            # denominator are assigned during the initialization, there is no
            # need to re-evaluate these attributes
            self._int = None
            self._decimal = None
            self._float = None
            self._repr = None

    @property
    def numerator(self):
        return self._numerator
    
    @property
    def denominator(self):
        return self._denominator

    @property
    def decimal(self):
        if self._decimal is None:
            self._decimal = self._decimal_repr()
        return self._decimal

    def reciprocal(self):           # Returns the reciprocal of the instance, if it exists (denominator != 0)
       return frac(self._denominator, self._numerator)

    # Returns the decimal representation of the fraction as a string
    # Examples:
    # 4/2    -->   2.0
    # 1/5    -->   0.2
    # 1/6    -->   0.1_6...             (to denote 0.1666...)
    # 1/3    -->   0.3...
    # 22/7   -->   3.142857...
    # 22/700 -->   0.03_142857...       (to denote 0.03142857142857... or 0.03(142857)...)
    def _decimal_repr(self):
        a = self._numerator
        b = self._denominator

        pre_decimal_string = str(a // b) + "."
        a %= b

        if a == 0:      # If 'b' completely divides 'a'
            return pre_decimal_string + "0"

        places, digits = self._decimal_helper(b)
        n = a * 10**places              # To evaluate the non-repeating part
        non_repeating_string = ""
        if places:                      # If there is a non-repeating part
            non_repeating_string = str(n // b).zfill(places) + "_"
        if digits:                      # If there is a repeating part
            repeating_string = str(((n % b) * 10**digits) // b).zfill(digits)
            return pre_decimal_string + non_repeating_string + repeating_string + "..."

        return pre_decimal_string + non_repeating_string[:-1]


    def _float_repr(self):
        # Passes at least 16 decimal places to the float function, and
        # at least one cycle of the repeating digits, if they exist
        decimal_string = self.decimal
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
 
    def __repr__(self):
        if self._repr is None:
            self._repr = "Fraction " + str(self._numerator) + " by " + str(self._denominator)
        return self._repr

    @staticmethod
    def _try_conversion(other):      # Attempts to convert 'other' to a 'frac' object with a try...except clause
        if isinstance(other, frac):
            return other
        try:
            return frac(other)
        except FractionError:
            raise TypeError(f"{type(other)} object can't be interpreted as a 'frac' object")

    def __eq__(self, other):        # Implements a == b 
        other = self._try_conversion(other)
        return self._numerator == other._numerator and self._denominator == other._denominator

    def __lt__(self, other):        # Implements a < b
        other = self._try_conversion(other)
        return self._numerator*other._denominator < other._numerator*self._denominator

    def __le__(self, other):       # Implements a <= b
        return self < other or self == other

    def __gt__(self, other):        # Implements a > b
        other = self._try_conversion(other)
        return self._numerator*other._denominator > other._numerator*self._denominator

    def __ge__(self, other):       # Implements a >= b
        return self > other or self == other

    def __ne__(self, other):        # Implements a != b
        return not self == other

    def __add__(self, other):       # Implements a + b
        other = self._try_conversion(other)
        return frac(self._numerator*other._denominator + self._denominator*other._numerator, self._denominator*other._denominator)

    def __mul__(self, other):       # Implements a * b
        other = self._try_conversion(other)
        return frac(self._numerator*other._numerator, self._denominator*other._denominator)

    def __radd__(self, other):      # Implements b + a
        return self + other
    
    def __rmul__(self, other):      # Implements b * a
        return self * other

    def __int__(self):              # Implements int(a)
        if self._int is None:
            self._int = self._numerator // self._denominator
        return self._int

    def __float__(self):            # Implements float(a)
        if self._float is None:
            self._float = self._float_repr()
        return self._float

    def __truediv__(self, other):       # Implements a / b
        other = self._try_conversion(other)
        return self * other.reciprocal()

    def __rtruediv__(self, other):      # Implements b / a
        other = self._try_conversion(other)
        return other / self
    
    def __neg__(self):                # Implements -a
        return frac(-self._numerator, self._denominator)

    def __pow__(self, other):       # Implements a**b
        return frac(self._numerator ** other, self._denominator ** other)

    def __rpow__(self, other):      # Implements b**a
        return other ** float(self)

