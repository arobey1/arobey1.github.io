---
title: "Math operations"
date: 2022-12-24
module: fundamentals
lesson: 2
draft: true
mathjax: true
---

Welcome back!  I hope you learned something new in the previous lesson on [variables]({{< ref "/python/variables.md" >}} "Variables").   Today, we are going to shift our focus to math.  And if that makes you a bit nervous, don't worry!  We won't be doing anything complicated today.  You'll just need the basics: addition, subtraction, exponents, and the like.

---

### The basic operations

Since we're talking about math in this lesson, we're largely going to focus on numerical data types; that is, ints and floats.  In the previous lesson, we learned all about how to create and compare these data types.  But as you'll see, there is so much more that we can do with Python variables.  In particular, in this lesson, we'll focus on answering the following question: What if we want to do *operations* on two or more values or variables?  For example, how do we add two variables in Python?

As we foreshadowed in the first lesson on [interacting with Python]({{< ref "/python/interacting_with_python.md#user-supplied-input" >}} "Interacting with Python"), adding two numbers works exactly as you'd expect in Python.

```python
>>> 1 + 1
2
```

Similarly, we can subtract, multiply, and divide numbers in the following way:

```python
>>> 5.0 - 3.1   # subtraction
1.9
>>> 7 * 3       # multiplication
21
>>> 20 / 8      # division
2.5
```

Note that this works for both floats and ints.  Hopefully these operations seem relatively intuitive.  One more operation that you should know is exponentiation, i.e. raising one number ot the power of another number.  Exponentiation is performed by writing two asterisks.  Here are some examples:

```python
>>> 2 ** 2          # 2 to the power of 2, i.e. 2 squared
4
>>> 25 ** 0.5       # 25 to the power of 0.5, i.e. the square root of 25
5.0
>>> 3 ** -1         # 3 to the power ot -1, i.e. 1/3
0.3333333333333333  
```

And that's basically it.  These five operations (and their symbols) -- addition (+), subtraction (-), multiplication (*), division (\\), and exponentiation (**) -- will cover a large portion of the math you'll need to do in Python.  There's a lot more to say about these operations, but before we move on, I think a few exercises are in order.

---

#### Exercise 1 (Using the basic operations)

Your first challenge for today is to write a script called moon_weight.py that calculates what you'd weigh on the (capital M) Moon.  Objects on the Moon weight about 16.6\% of what they'd weigh on Earth, so if you weight 200 lbs on Earth, you'd weight 33.2 lbs on the Moon.  Here's the kind of output I'm looking for:

```shell
$ moon_weight.py
This program calculates what you would weigh on the Moon.
Please enter your weight on the Earth.

Earth weight: 200
Enter units: lbs
On the Moon, you would weigh 33.2 lbs
```

If you're feeling ambitious, why not add a few more planets (well, the Moon isn't really a planet I guess, so let's humor the inner poet in each of us and say "celestial bodies" instead)?  For example, if you were standing on the surface of the Sun (not that I necessarily recommend doing so), you'd weigh 2707.2\% of what you weight on Earth.  This [website](http://www.seasky.org/solar-system/planet-weight-calculator.html) will give you the conversion rates for various other celestial bodies so that you can create output in a new script called celestial_bodies.py that work like this:

```shell
$ celestial_bodies.py
This program calculates what you would weigh on the moon.
Please enter your weight on the Earth.

Earth weight: 200
Enter units: lbs
On the Moon, you would weigh 33.2 lbs
On the Sun, you would weigh 5414.4 lbs
On Jupiter, you would weigh 472.8 lbs
```

Hint: In this exercise, you'll want to use Python's [input function]({{< ref "/python/interacting_with_python.md#user-supplied-input" >}}) as well as [f-strings]({{< ref "/python/variables.md#printing-variables-with-f-strings" >}}).

---

### Interlude: A break from math

This interlude is just for fun.  It doesn't use any math, but it does loosely fit within the confines of the lesson plan today.  Over the course of this lesson, you may have been wondering: What happens when I use the mathematical operations on other kinds of data types, e.g., strings and bools?  

In general, mathematical operations cannot always be applied to strings and bools.  For example, the following lines of code will throw errors:

```python
>>> "3" + 2
>>> "What is your favorite number" - 5
>>> True / False
>>> "I'll see your bid, and I'll" ** "you 5 dollars"
```

However, there are a few cases where mathematical operations can be combined with strings and bools.  Here's an exhaustive list with examples:

Two (or more) strings can be added together:

```python
>>> "Can " + "I " + "be " + "your " + "neighbor?"
Can I be your neighbor?
```

Strings can be multiplied by integers:

```python
>>> '¯\_(ツ)_/¯' * 3
¯\_(ツ)_/¯¯\_(ツ)_/¯¯\_(ツ)_/¯ 
```

When any of the mathematical operations we've seen are applied to bools, True is interpreted as 1 and False is interpreted as 0.  Thus:

```python
>>> True + False        # interpreted as 1 + 0
1
>>> False / True        # interpreted as 0 / 1
0.0
```

And that's it!  Now you know all there is to know about combining mathematical operations with strings and bools.


---

### Combining multiple operations

Almost all of the examples that we've seen thus far have involved only a single operation.  However, as as you'd expect, you can combine as many operations together as you'd like:

```python
>>> num_strawberries = 5
>>> num_oranges = 3
>>> num_tomatoes = 7
>>> num_strawberries + num_oranges + num_tomatoes
15
```

To break up compound mathematical expressions like the one shown above, it's often helpful to insert parenthesis like so:

```python
>>> (num_strawberries + num_oranges) + num_tomatoes
15
```

One reason we break up expressions like this with parenthesis is to make them more readible.  Above, the parenthesis are used to separate the addition of the number of fruits from the number of vegetables.

---

#### Exercise 2 (Preview of the order of operations)

This being said, it's important to be careful when combining multiple mathematical operations using parentheses.  Let's illustrate some of the trouble that can arise when we're not careful with how we write compound mathematical expressions.

Below I've written two expressions in the Python shell.  What do you think the output will be for each of these expressions?

```python
>>> (2 * 3) + 4
>>> 2 * (3 + 4)
```

After you've thought a bit about it, try executing these commands.  Did your expectation align with the output you see?

---

### The order of operations

As the above exercise illustrated, the order in which you write your mathematical operations matters in Python.  To govern which expressions should evaluated first, the order of operations in Python follows a specific set of guidelines known in technical jargon as the [operation precedence rule](https://docs.python.org/3/reference/expressions.html#operator-precedence).  In essence, this precedence rule creates a hierarchy amongst the operations that we met earlier in this lesson.  And without further adieu, here's that hierarchy:

1. **P**arentheses
2. **E**xponentiation
3. **M**ultiplication
4. **D**ivision
5. **A**ddition
6. **S**ubtraction

Some people like to remember this via the abbreviation PEMDAS,  which I've indicated by highlighting the first letter of each word in the hierarchy.

Here's how the hierarchy works.  Let's say I have a long, complicated mathematical expression, e.g., 

```python
>>> ((3 + 2) * 10 / 2) ** 0.5
```

How will Python execute this?  Well, according to the hierarchy, it will start the operation highest up on the list; in this case, that means the parentheses.  And importantly, Python will always start with the inner-most set of parentheses, meaning that `(3 + 2)` will be evaluated first.  Thus, we can imagine that `(3 + 2)` will be replaced by 5 in the above expression, leaving Python to consider the following simplified formula:

```python
>>> (5 * 10 / 2) ** 0.5
```

Following this, Python will proceed to look at the remaining set of parenthesis around `5 * 10 / 2`.  As multiplication comes earlier in the hierarchy than division, Python will first calculate `5 * 10`, leaving us with

```python
>>> (50 / 2) ** 0.5
```

Next, Python will perform the divion in the parentheses, yielding

```python
>>> 25 ** 0.5
```

As there is only one operation left, Python can now easily return the correct answer: 5.0.  Thus, the expected output of our original command is as follows:

```python
>>> ((3 + 2) * 10 / 2) ** 0.5
5.0
```

And at a high level, that's all you need to know about the hierachy of operations in Python.  To get some more practice with this idea, try out the following exercise.

---

#### Exercise 3 (More practice with the basic operations)

It's cold today (December 24, 2022).  Like really cold.  In fact, [it may be the coldest day of the year](https://www.poetryfoundation.org/poems/53219/mayakovsky).  And the way I see it, this cold weather gives us the perfect opportunity for a fun little exercise.  Let's use Python to calculate the *windchill* given the temperature ($T$) in degrees Fahrenheit and wind speed ($W$) in miles per hour.  Windchill is calculated using the following formula:

$$ \text{windchill} = 35.74 + (0.6215 \cdot T) - 35.75 \cdot W^{0.16} + 0.4275 \cdot T \cdot W^{0.16}$$

(Please don't ask me where this comes from; I have simply no idea. . .  Ok fine, I looked it up.  Dear reader, if you're interested, feel free to [peruse](https://en.wikipedia.org/wiki/Wind_chill#North_American_and_United_Kingdom_wind_chill_index) at your leisure.)

Your job is to write a script called calc_windchill.py that takes the temperature and wind speed as input, and then prints out the windchill.  Here's what I'm looking for:

```shell
$ python calc_windchill.py
Enter the temperature (in degrees Fahrenheit): 20
Enter the wind speed (in miles per hour): 10
The windchill is: 6.21888526608 degrees Fahrenheit.
```

If you insist on doing this like the rest of the world, fell free to rewrite this script so that it calculates the windchill in degrees Celsius rather than Fahrenheit.

---

### Exercise 4 (Pretest: data types and mathematical operations)

Here's a question for you: What determines the data type that is returned from a mathematical operation in Python?  For instance, in the code snippet from the earlier section on [the order of operations](#the-order-of-operations), why did 

```python
>>> ((3 + 2) * 10 / 2) ** 0.5
```

return 5.0 -- a float -- instead of 5 -- and int?  Before I fill you in, I want you to play around with this idea a little bit.  Try out the following commands, but before you hit enter, try to predict what the data type of the output will be.

```python
>>> 3 + 2.0
>>> 20 / 3
>>> 3 ** 3.1
>>> 0 * 0.0
>>> 10 - 6
>>> 100 / 4
>>> 64 ** 0.5
```

Big props to you if you got all of these right!  If not, the next section will explain what's going on.

---

### A word about data types

When it comes to data types and mathematical expressions, here's a basic rule of thumb to keep in mind: For addition, subtraction, multiplication, and exponentiation, if you put two integers in, you'll get an integer out; if either or both of your inputs are floats, then you'll get a float as output.  Thus, for example, from the previous exercise, we get the following behavior

```python
>>> 3 + 2.0
5.0
```

I.e., a float is returned because one of the inputs (namely, 2.0) to the addition operation is a float.

The odd man out here is division.  As opposed to the other operations, when you perform division in Python, you will always get a float as output.  Thus, even though the inputs to 

```python
>>> 100 / 4
25.0
```

are both integers, Python returns the float 25.0.

---

### Converting between data types

In some cases, you may not be satisfied with the data type that is returned by a mathematical expression.  For instance, perhaps you'd like the expression

```python
>>> 100 / 4
25.0
```

to return an integer rather than a float.  Well, as you'd imagine, Python has a solution for this.  As I mentioned very briefly in the lesson on [interacting with Python]({{< ref "/python/interacting_with_python.md#user-supplied-input" >}} "Interacting with Python"), we can turn a float into an int with the `int` function.  That is, we can force Python to return an int in the above example in the following way:

```python
>>> int(100 / 4)
25
```

Note that if the argument to the int function has decimal places, the output will be rounded *down* to the nearest whole number.  Thus:

```python
>>> int(2.3)
2
>>> int(9.999)
9
```

There are similar functions for converting a data type to a float, string, and bool.  Here are some examples:

```python
>>> float(5)
5.0
>>> str(5.6)
'5.6'
>>> bool(1)
True
```

Note that the `bool` function will only return 0 if the argument passed to it is zero.  For any other input, be it a string, integer, or float, as long as it isn't 0 or 0.0, `bool` will return True.

And that will just about do it for this lesson!  Stick around for a quick review and some additional exercises.

---

### Review

Let's summarize what we've learned in this lesson.

* [The basic operations](#the-basic-operations).  The following comprise the basic mathematical operations (and their symbols) in Python: addition (+),  subtraction (-), multiplication (*), division (\\), and exponentiation (**).

* [Exercise 1 (Using the basic operations)](#exercise-1-using-the-basic-operations).

* [Interlude: A break from math](#interlude-a-break-from-math).  In some cases, mathematical operations can be applied to bools and strings.  In particular, strings can be added together, and strings can be multiplied by integers.  When using any of the operations we've seen on bools, True is interpreted as 1 and False is interpreted as 0.

* [Combining multiple operations](#combining-multiple-operations).  Parentheses can be used to simplify mathematical expressions and to improve the readibility of your code.

* [Exercise 2 (Preview of the order of operations)](#exercise-2-preview-of-the-order-of-operations).  Care needs to be taken when using parentheses in mathematical operations, as they can change the outputs of these expressions.

* [The order of operations](#the-order-of-operations).  The order in which Python executes different mathemtical operations follows a hierarchy called the operations precedence rule.  The hierarchy follows the abbreviation PEMDAS, which stands for **p**arentheses, **e**exponentiation, **m**ultiplication, **d**ivision, **a**ddition, and finally, **s**ubtraction.  Operations higher up in the hierarchy will be executed before operations lower in the hierarchy.

* [Exercise 3 (More practice with the basic operations)](#exercise-3-more-practice-with-the-basic-operations).

* [Exercise 4 (Pretest: data types and mathematical operations)](#exercise-4-pretest-data-types-and-mathematical-operations)

* [A word about data types](#a-word-about-data-types).  When you perform addition, subtraction, multiplication, or division in Python, there are two possible cases: (a) if both of your inputs are integers, then an integer will be returned; (b) if either or both of your inputs are floats, then a float will be returned.  And as for division, regardless of the data types of your input, a float will always be returned.

* [Converting between data types](#converting-between-data-types).  The functions `int`, `float`, `str`, and `bool` can be used to convert between data types.

---

### Additional exercises

#### Exercise 5 (More practice with operations)

Remember those formulas that you learned in primary school about the volume and surface area of different objects?  I bet you didn't think that you'd ever see those again.  Well, today's the day that they come back to haunt you.  Recall that the volume $V$ and surface area $A$ of a sphere (in three dimensions) is

$$V = \frac{4}{3}\pi R^3 \quad\text{and}\quad A = 4 \pi R^2$$

where $R$ is the radius of the sphere and $\pi=3.1415926\dots$ is everyone's favorite mathematical constant.  Your job is to write a script called sphere.py that will take the radius of a sphere as input and return the volume and surface area of that sphere.  Here's some sample output:

```shell
$ python shell.py
Enter a radius: 10
Enter your approximation of pi: 3.1415926

Your sphere has a surface area of 1256.63704 units.
Your sphere has a volume of 4188.790133333333 units.
```