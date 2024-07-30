# Fractions

A data type to simulate fractions in Python

## Origin

Consider the following piece of code.
```python
>>> 0.1 + 0.1 + 0.1
0.30000000000000004
```

This is a consequence of how floating point numbers are stored in a computer's memory.

Instead, if the decimal 0.1 was stored as a fraction with it's numerator as 1 and denominator as 10, and then the addition operation was resolved into adding the three fractions 1/10, the result would be the fraction 3/10, whose floating point representation would be 0.3, as one would expect. This was the motivation behind this project.


## How to use

To get started with using the data type, import all of the module's contents.

```python
>>> from frac_latest import *
```

There are various ways to define a fraction, as highlighted by the `frac` class's docstring
```python
>>> print(frac.__doc__)
Fractions

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
            frac('0.6...')
            frac('0.1_3...')*1/frac('0.2')
            frac(3, frac('2.0')).reciprocal()
            frac('-2/3', -1)
            frac('2/3', 1.0)
            frac('2/3', '1')
            frac('0.6...')
            frac('0.6...', 1)
            frac('0.6...', '1.0')
            frac('-0.6...', '1/-1')

    Invalid arguments for the initialization raise a FractionError
```

The following operators work with `frac` objects.
```
- Equal to                      ==
- Less than                     <
- Less than or equal to         <=
- Greater than                  >
- Greater than or equal to      >=
- Not equal to                  !=
- Addition                      +
- Subtraction                   -
- Negation (unary)              -
- Multiplication                *
- Division                      /
- Exponentiation                **
```

Something interesting is that every time a unique new fraction object is created, it's stored in a dictionary so that if another fraction with the same numerator and denominator is required, the stored fraction is simply extracted from the dictionary and returned. This makes things more efficient. Below is a demo of the same
```python
>>> x = frac(1, 2)
>>> y = frac(10, 20)
>>> x is y            # Returns id(x) == id(y)
True
```

`numerator` and `denominator` are properties. This means that they can be accessed but assigning to them won't work. This is because this data type is meant to be **immutable**.
```python
>>> x = frac(220, 70)
>>> print(x.numerator)        # 220/70 has been simplified to 22/7
>>> x.numerator = 1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: property 'numerator' of 'frac' object has no setter
```

`decimal` is another property, and a very important one. I'd call the decimal representation features the highlights of the data type (converting a fraction to it's decimal representation and converting the decimal representation to a fraction).<br>

If the decimal representation terminates, then the usual floating-reprensentation is returned. If all of the digits after the decimal repeat, then the first set of non-repeating digits is displayed, followed by `...`<br>
If some digits after the decimal aren't repeated, they are followed by a `_`, and then the first set of repeating digits, again followed by `...`


The following demonstrate each of these
```
4/2     -->     2.0
1/5     -->     0.2
1/3     -->     0.3...
1/6     -->     0.1_6...
22/7    -->     3.142857...
22/700  -->     0.03_142857...
```

In case the repeating digits exceed `frac.max_repeating_digits` (2000 by default), the repeating digits are truncated to the first `frac.max_repeating_digits`. A warning is shown whenever this happens. You can change the max digits as follows
```python
>>> frac.max_repeating_digits = 10000
```

The decimal representation isn't often something that can be represented as a `float` object, due to the presence of `_` and `...`<br>
Due to this, the `decimal` attribute returns a `str` object. To get the corresponding `float` value, call the in-built `float` function with the `frac` object as a parameter, which will end up calling `frac.__float__`.
```python
>>> x = frac(1, 6)
>>> y = float(x)
>>> print("The floating point representation of", x, "is", y)
The floating point representation of 1/6 is 0.1666666666666666
```

`my_frac.reciprocal()` returns a `frac` object equivalent to `my_frac`'s reciprocal

```python
>>> x = frac(31, 41)
>>> y = x.reciprocal()
>>> print(y.numerator, y.denominator)
31 41
>>> print(f"{x} times {y} is {x*y}")
31/41 times 41/31 is 1/1
```

### Examples

<p align = "center"> $\displaystyle\sum_{i=1}^\infty \dfrac1{2^i} = \dfrac12 + \dfrac14 +\dfrac18 +\cdots=1$ </p>

```python
>>> current_sum = 0
>>> for i in range(1, 1001):
...     current_sum += frac(1, 2**i)
...
>>> print(current_sum.decimal)          # Should ALMOST be 1
0.9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999066736381496781121009910455276182830382908553628291975378285660204033089024224365545559672902118897640405010069675757375784512478645967605158479182796069243765589333861674849726004924014098168488899509203734886881759487485204066209194821728874584896189301621145573518880530185771339040777982337089557201543830551112852533471993671631547352570738170137834797206804710506392882149336331258934560194469281863679400155173958045898786770370130497805485390095785391331638755207047965173135382342073083952579934063610958262104177881634921954443371555726074612482872145203218443653596285122318233100144607930734560575991288026325298250137373309252703237464196070623766166018953072125441394746303558349609375
>>> print(float(current_sum))
1.0
```
< More examples to come >
