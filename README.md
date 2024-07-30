# Fractions

A data type to simulate fractions in Python
<br><br>

## Origin

Consider the following piece of code.
```python
>>> 0.1 + 0.1 + 0.1
0.30000000000000004
```

This is a consequence of how floating point numbers are stored in a computer's memory.

Instead, if the decimal 0.1 was stored as a fraction with it's numerator as 1 and denominator as 10, and then the addition operation was resolved into adding the three fractions 1/10, the result would be the fraction 3/10, whose floating point representation would be 0.3, as one would expect. This was the motivation behind this project.<br>

I'm aware of the performance issues that come with this, but this project was a great opportunity for me to make use of my knowledge of Python's classes. Speaking of that, `frac_setattr_artifact.py` isn't a part of the latest version of this program, but it was an interesting approach, so I decided to keep it in the repo.<br>

This project has evolved a lot and I've tried my best to comment and document it properly all along. I've thoroughly enjoyed developing this. I'm thinking of implementing this in C++ some day, and then performing some time tests with respect to the examples given below and more. When I do that, I'll leave a link to the same here.<br>

Enjoy reading through this document!
<br><br>

## How to use

To get started with using the data type, import all of the module's contents.

```python
>>> from frac import *
```
<br>

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
<br>

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
<br>

Something interesting is that every time a unique new fraction object is created, it's stored in a dictionary so that if another fraction with the same numerator and denominator is required, the stored fraction is simply extracted from the dictionary and returned. This makes things more efficient. Below is a demo of the same
```python
>>> x = frac(1, 2)
>>> y = frac(10, 20)
>>> x is y            # Returns id(x) == id(y)
True
```
<br>

If for some reason, you want to empty this dictionary, you can execute `frac.clear_instance_space()`.<br>
However, it's important to note that emptying this dictionary won't delete the previously created `frac` objects from memory. The following code should demonstrate this
```python
>>> x = frac(1, 10)
>>> print(frac._instance_space)         # Current instance space
{(1, 10): Fraction 1 by 10}
>>> frac.clear_instance_space()         # frac._instance_space is an empty dictionary now
>>> print(frac._instance_space)
{}
>>> print(x)                            # Still works
```
<br>

`numerator` and `denominator` are properties. This means that they can be accessed but assigning to them won't work. This is because this data type is meant to be **immutable**.
```python
>>> x = frac(220, 70)
>>> print(x.numerator)        # 220/70 has been simplified to 22/7
>>> x.numerator = 1
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: property 'numerator' of 'frac' object has no setter
```
<br>

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
<br>

In case the repeating digits exceed `frac.max_repeating_digits` (2000 by default), the repeating digits are truncated to the first `frac.max_repeating_digits`. A warning is shown whenever this happens. You can change the max digits as follows
```python
>>> frac.max_repeating_digits = 10000
```
<br>

The decimal representation isn't often something that can be represented as a `float` object, due to the presence of `_` and `...`<br>
Due to this, the `decimal` attribute returns a `str` object. To get the corresponding `float` value, call the in-built `float` function with the `frac` object as a parameter, which will end up calling `frac.__float__`.
```python
>>> x = frac(1, 6)
>>> y = float(x)
>>> print("The floating point representation of", x, "is", y)
The floating point representation of 1/6 is 0.1666666666666666
```
<br>

`my_frac.reciprocal()` returns a `frac` object equivalent to `my_frac`'s reciprocal

```python
>>> x = frac(31, 41)
>>> y = x.reciprocal()
>>> print(y.numerator, y.denominator)
31 41
>>> print(f"{x} times {y} is {x*y}")
31/41 times 41/31 is 1/1
```
<br><br>

### Examples

<p align = "center"> $\Huge 3\times0.1 = 0.3$ </p>

```python
>>> 3*0.1
0.30000000000000004
>>> print(3*frac(0.1))
3/10
>>> print(float(3*frac(0.1)))
0.3
```
<br>

<p align = "center"> $\Huge 4\displaystyle\sum_{i=0}^\infty \dfrac{(-1)^n}{2i+1}=\pi$ </p>

```python
>>> my_pi = 0
>>> # The for loop that follows takes some time
>>> for i in range(10000):
...     my_pi += frac((-1)**i, 2*i+1)
...
>>> my_pi *= 4
>>> print(my_pi.decimal)                # Gives a warning about the repeating digits' truncation
Warning: Repeating digits truncated to 2000
Use frac.max_repeating_digits to change
3.141492_65359004323845951838337481537878701364274418046051347980547439567069002885087063294318676551571244918027087959521665613834672305324085742516537014547652366702419402485256552534094998793885940729109008436960753359009301135666753647438319623229441612446521297340273756021890283254559891111492176330912349454672513763979442121125978076927077435016616662935019672111854189127606086682361945665191950342807497442180642497167958999586312097658827905254271784068077646258550478228190675931985918005454082317980652527202404590203763314788865314550108120317712317168728056012858262996729099567566169115759027156277771445748832872952336639705455951762777472299429665682637954317801971169394304194088831335065669354017205173899379985672619954322292937041965168291152032598333199980659928584626689448428981404765116638262023690591910691689153021477842839556453438060982645950202065895181330299861402241985892119704454744587734161657805796093156787545902131486078683392873795447023547563806590048620861224610344637723504793691472376941063860938203232238039596177396932612283313723462539403214565777584381864886860497747101210892110273711129809924728625844745820722807887294624910153300312161093805836544138124139330652736059695486409779063707211112028690890970239923480571036306713827290069103730763442202563040002389091581815595188490656896659865444268251963592172034259841327255975100498933023265315474832694752036419950152251939966392421363971466105558291605008561418840873134773302423050329113232109375257890282359366562912169063275658800714327520824941889087819123522719471459190190634222584113652842751752990838501391633487612372489595754390933212457797519404158159457094015097321107701502230928127941685365669764374943034837029206657209293381438913613924681970573077953893565893006250652431712562765277109045551557829886600860740602664625686807026232531872852252094343500694612711861346815658238528886310211875410319449198169085850806854408612647848134263822678842101385497612642299733678548650245368246244...
>>> print(float(my_pi))
3.1414926535900434
```
<br>

<p align = "center"> $\Huge \displaystyle\sum_{i=1}^\infty \dfrac1{2^i} = \dfrac12 + \dfrac14 +\dfrac18 +\cdots=1$ </p>

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

### Note

`frac.py` has the latest version of the program
`frac_setattr_artifact.py` is what the program looked like at a certain stage where I thought of defining a `__setattr__` method to work around some issues
`testing.py` is a basic showcase of some operations with `frac` objects
`examples.py` has code related to the [examples](https://github.com/rajdeep-314/python_fractions/tree/main#examples) above, among a few others
