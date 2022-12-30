---
title: "Lists"
date: 2022-12-26
module: fundamentals
lesson: 4
draft: true
mathjax: true
---

You're back!  We've got a lot to cover in this lesson, so let's get right into it.  The goal is introduce another fundamental data type: the list.  Lists are crucial to almost every programming language out there, and Python is no excetpion.

---

### A motivating example: Why we need lists in Python

Let's say that you're an avid reader.  You read all sorts of things.  Technical books, novels, the occasional murder mystery, biographies, poetry, you name it!  But here's the problem.  You encouter so many books that you can't remember them all.  And so you'd like some way of remembering the books you've seen so that one day, you can head to your local bookstore and buy to your heart's content.  

Ideally, we'd like to be able to save a list of books in a variable so that we can look back at it later.  Sadly, we haven't yet met a data type that can handle such a task.  One hacky solution would be to write a long Python string, for which Python has a special syntax:

```python
>>> myBooks = (
    "How to Do Nothing: Resisting the Attention Economy" \
    "Norwegian Wood" \
    "Optimization for Data Analysis" \
    "A Tale for the Time Being"
)
>>> print(myBooks)
'How to Do Nothing: Resisting the Attention EconomyNorwegian WoodOptimization for Data AnalysisA Tale for the Time Being'
```

Hopefully it's clear why this isn't a great solution. For starters, t's won't be easy to add or remove books from this reading list.  Furthermore, the books are also all smushed together, which will make things harder when I'm trying to quickly look through the titles.  Ideally, I'd like to be able to have each book saved as a separate value, and I'd like to have a straightforward way to iterate through and update this list.  

These needs set the stage for our new data type: the list.

---

### Lists in Python

Lists are one of the most important data types in any programming language.  

> **Lists** allow you to store multiple values in a single variable. 

The sytax is quite straightforward.  Returning to our earlier example, we can create a list to store my reading list as follows:

```python
>>> myBooks = [
    "How to Do Nothing: Resisting the Attention Economy", 
    "Norwegian Wood", 
    "Optimization for Data Analysis", 
    "A Tale for the Time Being"
]
>>> print(myBooks)
['How to Do Nothing: Resisting the Attention Economy', 'Norwegian Wood', 'Optimization for Data Analysis', 'A Tale for the Time Being']
```

The square brackets signify that this variable is a list, and each item in a list is separated by a trailing comma.  Lists can contain any of the other data types we've met so far.  For example, all of the following are valid lists:

```python
>>> fruits = ['apple', 'banana', 'pear']
>>> numbers = [32, 15, 3, 6, 9, 33]
>>> miscellaneous = ['a', True, 'fantastisch', 5.432]
```

Recalling what we learned about the [type function]({{< ref "/python/variables_data_types.md#exercise-1-review-of-data-types" >}} "Type function"), we can call the type function on any of the variables we created above to confirm that they have the 'list' data type:

```python
>>> type(fruits)
<class 'list'>
```

Before talking more about lists, here's an exercise to get some more practice with lists.

---

#### Exercise 1 (Creating lists)

Let's start with something simple.  Write a script called my_favorites.py to make a list of all of your favorite things.  Your script should accept inputs from the user, and then put those inputs into a list.  Here's what mine would look like:

```shell
$ python my_favorites.py
Enter your favorite color: orange
Enter your favorite number: 23
Enter your favorite sports team: Arsenal
Enter your favorite activity: crossword puzzles

Here's a list with all of your favorite things:
['orange', 23, 'Arsenal', 'crossword puzzles']
```

---

### Indexing into a list

Lets return to our motivating example, wherein we created a list variable called `myBooks` containing four different titles.  Let's say that I've read the first two books in my list -- "How to Do Nothing: Resisting the Attention Economy" and "Norwegian Wood" -- and now I'm ready to start the third book.  How can I pull out the third book from my list?

To answer this question, we need to talk about indexing.  When I create a list, each item in that list has what's known as an index.

> An index specifies the position of an item in a list.

Indices in Python start from 0, and they are read from left to right.  So in the `myBooks` example, the index of "How to Do Nothing: Resisting the Attention Economy" would be 0, the index of "Norwegian Wood" would be 1, and so on.  

In Python, there is a simple syntax for retreiving an item at a particular index in a list.  For instance, to retreive each item in `myBooks`, I can write the following:

```python
>>> print(myList[0])
'How to Do Nothing: Resisting the Attention Economy'
>>> print(myList[1])
'Norwegian Wood'
>>> print(myList[2])
'Optimization for Data Analysis'
>>> print(myList[3])
'A Tale for the Time Being'
```

It may be slightly unintuitive that Python's indexing scheme starts from zero (instead of one), but over time, this will become second nature to you.  

---

#### Exercise 2 (Indexing into lists)

In a script called retreive_items.py, create a list called `my_special_list` and save any list you want in this variable.  For example, in my version of retreive_items.py, `my_special_list = ['Hungry', 'hungry', 'hippos']`.  Start by printing that list out to the console, and then ask a user for an index for your list.  Then print out the item at that index in `my_special_list`.  Your output should look something like this:

```python
$ python retreive_items.py
Your list is: ['Hungry', 'hungry', 'hippos']
Enter an index: 2
The item at index 2 is: hippos
```

Hint: Recall that the input function saves whatever you input as a string, so you'll need to use the `int` function to turn your input into an integer.

---

### Methods on lists

Now that we've got the hang of creating lists and indexing into them, let's talk about some of the operations we can do on lists.  In this section, we'll discuss five of the most useful list operations.

**Length.** One of the most basic list operations is to determine how many items are in a list, a quantity that is commonly known as a list's length.  

> The length of a list is the number of elements in that list.

To calculate the length of a list, we can use the `len` function:

```python
>>> musketeers = ['Athos', 'Porthos', 'Aramis']
>>> print(len(musketeers))
3
```

**Append.**  Also popular is the `append` method, which allows you to add a new element to the end of a list.  Here it is in action:

```python
>>> title = ['Harry', 'Potter', 'and', 'the', 'Deathly']
>>> title.append('Hallows')
>>> print(title)
['Harry', 'Potter', 'and', 'the', 'Deathly', 'Hallows']
```

**Insert.**  Sometimes, rather than adding an item to the end of a list, we may want to insert a value into a list at a particular index.  This can be accomplished using the `insert` method, which takes two arguments: an index and a value.  For example:

```python
>>> lyrics = ['Row', 'row', 'row', 'boat']
>>> lyrics.insert(3, 'your')
>>> print(lyrics)
['Row', 'row', 'row', 'your', 'boat']
```

As you can see, this function inserts 'your' so that `lyrics[3] = 'your'`.  

**Reverse.**  Another fun way to manipulate a list is to reverse the order of its items.  A list can be reversed via the `reverse` method:

```python
>>> greek = ['alpha', 'beta', 'gamma']
>>> greek.reverse()
>>> print(greek)
['gamma', 'beta', 'alpha']
```

**Pop.**  And finally, the `pop` method will allow you to remove elements from your list.

```python
>>> pets = ['bunny', 'cat', 'dog', 'tiger', 'hampster']
>>> pets.pop(3)
>>> print(pets)
['bunny', 'cat', 'dog', 'hampster']
```

The argument to the pop method specifies the index of the item to remove.  In this case, since we passed the number 3 as an argument to `pop`, the item at index 3 was removed (in this case, 'tiger').

---

#### Exercise 3 (It's almost like Wordle!)

Do you guys know [Wordle](https://www.nytimes.com/games/wordle/index.html)?  That game where you have like five guesses to figure out what a secret word is.  Yeah, it's not my favorite, but lots of people swear by it.

In this exercise, we're going to do something that's a cross between Wordle and a [word ladder](https://en.wikipedia.org/wiki/Word_ladder).  Here's the game.  I am going to give you a list of characters that spells a word.  Your job is to use the methods we met above to transform the first word into the second word.  For example, let's say our starting word is `['g', 'r', 'e', 'e', 'n']` and our ending word is `['e', 'g', 'r', 'e', 't']`.  The following sequence of commands can transform the first word into the second.

```python
>>> start_word = ['g', 'r', 'e', 'e', 'n']
>>> end_word = ['e', 'g', 'r', 'e', 't']
>>> start_word.insert(0, 'e')
>>> print(start_word)
['e', 'g', 'r', 'e', 'e', 'n']
>>> start_word.pop(5)
>>> print(start_word)
['e', 'g', 'r', 'e', 'e']
>>> start_word.pop(4)
['e', 'g', 'r', 'e']
>>> start_word.append('t')
>>> print(start_word)
['e', 'g', 'r', 'e', 't']
>>> start_word == end_word
True
```

Here's your task.  I'll give you a few pairs of words, and you need to determine how to get from one sequence to another.  Good luck!

1. `start_word = ['d', 'r', 'a', 'w']` and `end_word = ['w', 'a', 'r', 't']`.
2. `start_word = ['h', 'e', 'l', 'l', 'o']` and `end_word = ['w', 'o', 'r', 'l', 'd']`.
3. `start_word = ['k', 'l', 'e', 'i', 'n']` and `end_word = ['k', 'a', 't', 'z', 'e']`.

---

### Slicing a list

Now that we've learned what indexing is, it's about time that we talked about slicing.  Slicing is like indexing on steroids.  

> Slicing allows you to select multiple elements from the same list.

For instance, let's say that I wanted to update `myBooks` to make a new reading list that only contains the last two books.  With indexing, I would have to do something like this:

```python
>>> thirdBook = myBooks[2]
>>> fourthBook = myBooks[3]
>>> newBookList = [thirdBook, fourthBook]
>>> print(newBookList)
['Optimization for Data Analysis', 'A Tale for the Time Being']
```

This works, but it isn't scalable.  If my reading list was much longer, this would take many more lines of code, since I need one line for each book I want to select.  

Luckily, slicing gives us a much faster way of solving this problem.  To slice the end of a list, I can do the following:

```python
>>> newBookList = bookList[2:]
>>> print(newBookList)
['Optimization for Data Analysis', 'A Tale for the Time Being']
```

Slicing a list is always characterized by one (or multiple) colons in the square brackets.  The 2 right before the colon means that the slicing operation will start from index 2 and slice off everything until the end of the list.

If, instead of slicing to the end of the list, we only wanted to slice off the middle two books, we can simply an index before and after the colon:

```python
>>> print(bookList[1:3])
['Norwegian Wood', 'Optimization for Data Analysis']
```

As you may have realized, there's a general principle at play here.  Let's say we have a list called `a`.  The rules of slicing in Python are as follows:

```python
>>> a[start:stop]  # items from start through stop-1
>>> a[start:]      # items from start through the end of the list
>>> a[:stop]       # items from the beginning through stop-1
>>> a[:]           # a copy of the whole array
```

The tricky part is that the `stop` argument will slice until index `stop-1`.  In time, this will become second nature to you.

---

#### Exercise 4 (Slicing and dicing)

If you thought that was neat, you're going to love this.  Slicing can get even more involved if you want to select items from a list according to a pattern, e.g., selecting all of the elements with an even or odd index.  Rather than illustrating how to use the syntax, I'm going to tell you the general principle, and leave it to you to try it out.  If, as before, we have a list called `a`, the general syntax for slicing is as follows:

```python
>>> a[start:stop:step]
```

This means that your slice will start at index `start`, end at index `stop-1`, and proceed with step size `step`.  Here's a sample output from the script -- which we'll call fancy_slicing.py -- that I want you to write:


```shell
$ python fancy_slicing.py
Your list is: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Enter "start" index: 1
Enter "stop" index: 8
Enter "step" index: 2

Your slice is: [1, 3, 5, 7]
```

Start by defining any list in a variable called `my_list`, and print that list out to the user.  I recommend using a list with a bunch of numbers in order, because it'll make it easier to see what's going on.  Prompt the user for a `start` and `stop` index as well as a `step` size.  Then print out what you get by slicing into `my_list` via the slicing operation: `my_list[start:stop:step]`.

Try this out with a bunch of combinations to get familiar with slicing in Python.  And make sure you keep fancy_slicing.py handy; we're going to need it in a couple of future exercises in this lesson.

---

### Meet the range function

When working on the previous exercise, did you think to yourself: Wouldn't it be nice if I didn't have to type out a list of numbers to create `my_list`?  Why doesn't Python have any functionality so that I can make a list like `[0,1,2,3,4,5,6,7,8,9]` really quickly?

Well, if you happened to have that thought, then you're in luck!  Python does have such a function, and it's called **range**. 

> The range function returns a sequence of numbers, which by default start from zero and come in increments of one, and stop at a user-specified number.

The `range` function is another crucial piece of Python that you'll see in almost every program you'll encounter.  Interestingly, the `range` function has a similar syntax to the syntax for slicing.  In general, `range` takes three arguments: a number to start the range, a number to end the range, and a step size.  Here are some examples:

```python
>>> list(range(0, 5, 1))
[0, 1, 2, 3, 4]
>>> list(range(3, 15, 2))
[3, 5, 7, 9, 11, 13]
```

Range is most often used to generate a sequence of numbers starting from zero.  To do this, one can simply call the following:

```python
>>> list(range(10))
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Note that just as with slicing, range will include numbers up `stop-1`.  Furthermore, you might have already noticed that we are wrapping the range function with the `list` function.  Like the `int`, `float`, `bool`, and `str` functions that we've met in the previous lesson on [Math operations]({{< ref "/python/interacting_with_python.md#converting-between-data-types" >}} "Interacting with Python"), the `list` function transforms other data types into lists.  When you call range without converting it to a list, you'll get something like this:

```python
>>> ls = range(3, 9, 4)
>>> print(ls)
range(3, 9, 4)
>>> type(ls)
<class 'range'>
```

You may have expected `range` to have the 'list' data type, but notice that 'range' is actually it's own type in Python.  Why is that?  If you're interested, read on; it not, there's a couple of exercises waiting for you down below. 

---

### Why range has its own type

Let's talk about where we are right now (circa December 2022).  The current version of Python is 3.10, which was released in October of 2021.  Rewinding all the way back to the early 2000s, Python 2 was the standard.  In Python 2, `range` returned a list, as one might expect.  However, problems started arise from `range` having this type.  To see why, consider the following code snippet:

```python
>>> big_number = 1000000000000000
>>> big_range = range(big_number)
```

If `range` directly created a list, when we create `big_range`, we would be creating a list with 1000000000000000 entries.  This can potentially take up *a lot* of space in memory, causing our code to slow down significantly.  

To avoid this, in Python 3, `range` now returns a what's known as a generator object, which does not need to store the entire list in memory.  This is far more efficient.  We'll talk more about this in a future lesson.

To close up this history lesson, I'll note that in 2020, Python 2 met what's known as it's "end of life" (sometimes abbreviated as EOL, meaning that it's not longer supported by the Python development team.  Just like codebases, programming languages are actively developed to provide more functionality, make them faster, and improve readibility.  

---

#### Exercise 5 (Making our life easier with range)

Let's go back to [Exercise 4](#exercise-4-slicing-forwards-and-backwards).  In this exercise, you created a variable called `my_list`.  Now that you've learned how range works, go back and update your code so that `my_list` is created using the `range` function.  

---

#### Exercise 6 (A slicing challenge)

Hopefully you completed the last exercise without too much trouble.  In this exercise, we're going to use the script you wrote in [Exercise 4](#exercise-4-slicing-forwards-and-backwards) and then updated in [Exercise 5](#exercise-5-making-our-life-easier-with-range) to test how well you've understood slicing.

So that we're on the same page, start by defining `my_list = list(range(10))`.  Next, I'm going to give you a sequence of sliced lists, and your job is to come up with the `start`, `stop`, and `step` inputs to your program that will return these slices.  Are you ready?

```python
>>> [0, 2, 4, 6, 8]
>>> [1, 3, 5, 7, 9]
>>> [1, 6]
>>> [3, 6]
>>> [1, 4, 7]
>>> [8]
```

---

### Strings? What does this have to do with strings?

This whole lesson has been about lists.  We've learned about indexing lists, applying functions to lists, and slicing lists.  Now, what if I told you that much of what we learned today applied not only to lists, but also to strings?  Yes, it's true!  

A string can be indexed and sliced in exactly the same way as a list.  For example:

```python
>>> myString = 'Die Essen ist sehr lecker!'
>>> print(myString[10])
'i'
>>> print(myString[0::2])
'DeEsnitsh ekr'
```

You can even turn a string into a list of characters:

```python
>>> string = 'Hello world!'
>>> list_string = list(string)
>>> print(list_string)
['H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!']
```

This can come in really handy in fields like bioinformatics, where one of the main goals is to find matching subsequences in long chains of base pairs.

---

### Review

Let's summarize what we've learned in this lesson.

* [A motivating example: Why we need lists in Python](#a-motivating-example-why-we-need-lists-in-python).  

* [Lists in Python](#lists-in-python).  The list data type in Python allows you to store multiple values in a single variable.

* [Exercise 1 (Creating lists)](#exercise-1-creating-lists)

* [Indexing into a list](#indexing-into-a-list).  The location of an item in a list is called it's index.  Indexing in Python starts from zero, and proceeds from left to right.

* [Exercise 2 (Indexing into lists)](#exercise-2-indexing-into-lists)

* [Methods on lists](#methods-on-lists).  We met five important operations that can be performed on lists: the `len` function calculates the length -- or number of elements -- in a list; the `append` method adds an item to the end of a list; the `insert` method inserts an item at a particular index; the `reverse` method reverses the order of the items in a list; and finally, the `pop` function removes the item at a particular index.

* [Exercise 3 (It's almost like Wordle!)](#exercise-3-its-almost-like-wordle).

* [Slicing a list](#slicing-a-list).  Slicing allows you to select multiple elements from the same list.  Given a list (say it's called `a`), slicing is performed by running `a[start:stop:step]`, where `start` is the starting index, `stop-1` is the ending index, and `step` is the step increment.

* [Exercise 4 (Slicing and dicing)](#exercise-4-slicing-and-dicing).

* [Meet the range function](#meet-the-range-function).  The range function returns a sequence of numbers.  By default, these numbers start at zero and are incremented by one.  The list ends at a user-supplied input.  The `list` function can transform variables of other data types into lists. 

* [Why range has its own type](#why-range-has-its-own-type).  If range returned a list data type, it would need to store the entire list it creates in memory.  When the list is very large, this can slow down your program.  To fix this, range returns a generator object, which does not need to store every part of the list in memory. 

* [Exercise 5 (Making our life easier with range)](#exercise-5-making-our-life-easier-with-range).

* [Exercise 6 (A slicing challenge)](#exercise-6-a-slicing-challenge).

* [Strings? What does this have to do with strings?](#strings-what-does-this-have-to-do-with-strings)  Many operations that work on lists, such as indexing and slicing, also work on strings.  The `list` function can be called on any string to turn that string into a list of characters.

---

<!-- ### Additional exercises

* List of lists

--- -->

Hopefully you feel more comfortable working with lists now than you did at the start of this lesson.  I'll see you in the next lessons on lists!



