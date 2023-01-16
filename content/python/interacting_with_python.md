---
title: "Interacting with Python"
date: 2022-12-19
module: introduction
lesson: 2
draft: true
---

### Interacting with Python

There are two main ways of interacting with Python: with a shell and with a script.  Here's a brief primer on how shells and scripts work and when you should use them.

---

#### Python shell

Perhaps the easiest way to start interacting with Python is through what's known as a **shell**.  Never heard of a shell before?  No worries!  Here's a quick definition:

> A shell is an interpreter that can execute Python programs and simple Python commands.

To open a shell, open a terminal (not sure what this is? see [this link](https://www.digitalocean.com/community/tutorials/an-introduction-to-the-linux-terminal)), type the word "python," and hit enter.  You should see something like this:

```shell
$ python
Python 3.9.6 (default, Jun 29 2021, 06:20:32) 
[Clang 12.0.0 (clang-1200.0.32.29)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

The three sideways carrots that you see at the bottom of the output are where you can execute Python commands.  Let's try it out!  It's [traditional](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) to print the words "Hello world!" in your console when you first start learning a programming language.  And who are we to break with tradition?  In your console, type the following statement:

```python
>>> print("Hello world!")
```

Now hit enter (or return, depending on your keyboard)!  You should see the worlds "Hello world!" printed out in the console, i.e.

```python
>>> print("Hello world!")
'Hello world!'
```

To exit the Python shell, you can type `exit()` and hit enter, or use Ctrl-D.

```python
>>> exit()
```

Congratulations!  You just executed your first Python expressions.  Here's to many more.

---


#### Python scripts

The second way to interact with a Python program is through what's known as a **script**.  

> A Python script is a file containing Python code.

The difference between a shell and a script is as follows.  In a shell, you can execute expressions one by one by typing typing them into the console and hitting enter.  In a script, you can write one or multiple expressions in the file, and then you can execute the code by running it in your console.  

For example, try creating a file called my_first_program.py.  How will your computer know that this is a Python file?

> All Python programs end with ".py".  This tells your operating system that the code your running is written in Python.

So now whenever you see a file ending in .py, you can impress your friends, colleagues, or partner by telling them that you're sure this is a Python script without needing to open the file!  

Next, add the following contents to my_first_program.py:

```python
print("Hello world!")
```

Now to run your program, open your terminal, and from the same directory as my_first_program.py, run the following command:

```shell
$ python my_first_program.py
```

And as before, you should see the following output.

```shell
$ python my_first_program.py
'Hello world!'
```

Now that you know what shells and scripts are, you might be wondering when you should use one over the other.  Well, I'm glad you asked!  

---

### When to use the shell and when to use scripts

All of the code in this set of notes can be executed in a shell or in a script.  That being said, for longer expressions or programs, it tends to be easier to use scripts.  Why?  There's a few reasons:

* **Organization.**  Scripts allow you to easily execute multiple expressions at once, whereas in the shell, expressions need to be executed one by one.  When you have a long program, it becomes much easier to organize your code into interpretable blocks when your statements are broken into one or several scripts.

* **Program state.**  Every time you exit and restart the shell, you lose all of the code that you've written.  In scripts, you can save your code by saving the file, and then rerun it whenever you want.

---

### Print statements

Let's talk a little bit more about the commands you executed above.  In both the shell and script programs that we wrote, we ran the command `print("Hello world!)`.  This command consists of two parts: a function called `print` and an argument that we passed to that print statement; namely, "Hello world!".

> The `print` function allows a user to print statements to the console.

You'll be using the print statement *a lot* when writing Python code, so to get you more familiar with it, let's look at a few examples in the Python shell.

```python
>>> print("I am using the print function")
'I am using the print function'
>>> print(3.1415926)
3.1415926
>>> print("23 is a prime number")
'23 is a prime number'
```

Let's take what you've learned about printing and apply it in the following exercise.

---

#### Exercise 1 (From the shell to a script)

The examples we just went through were all executed in a Python shell.  My question for you: Can you write this program as a script and produce the same output?  On your computer, create a script called print_examples.py and write a Python script that prints the same output.  That is, you should see the following in your terminal:

```shell
$ print_examples.py
'I am using the print function'
3.1415926
'23 is a prime number'
```

Think you've got the hang of printing?  Let's kick things up a notch in the next exercise.

---

#### Exercise 2 (Your first Python program)

These are early days.  You're just getting started on your Python journey.  But guess what!  You're ready to write your first original Python program.  Yes, really!  What will you be doing?  I want you to write a program called print_my_cow.py that prints the following output to the terminal.

```shell
$ python print_my_cow.py
^__^
(oo)\_______
(__)\       )\/\
    ||----w |
    ||     ||
```

If that's too easy for you, why not spruce things up a little bit?  Maybe your cow is a thoughtful cow, and you'd like to show her thinking up a funny (albeit heartfelt) witticism.

```shell
$ python print_my_cow.py
 _________________________
(   I udderly love you!   )
 -------------------------
        o   ^__^
         o  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```

Feel free to go crazy with this one.  (If you're wondering where I got this idea, have a look at the Linux package [cowsay](https://en.wikipedia.org/wiki/Cowsay)).

---

### User-supplied input

Another important part of programming is accepting input from a user.  In the previous two exercises, running your scripts always produced the same output.  But what if we wanted to have the output of our program depend on an input that the user supplies?

For example, let's say I wanted to write a program that takes a number as input and prints out that number incremented by one.  Easy enough!  I could just write the following in the shell.

```python
>>> my_favorite_number = 5
>>> print(my_favorite_number + 1)
6
```

But what happens when your favorite number changes from 5 to 941?  Well, you'd have to write the whole thing over again.  

```python
>>> my_favorite_number = 941
>>> print(my_favorite_number + 1)
942
```

This is a little bit cumbersome.  What we'd really like is to be able to run a program that accepts your favorite number as input and then prints the incremented number.   

How should we do this?  Well, hopefully you remember the tips in [When to use the shell and when to use scripts](#when-to-use-the-shell-and-when-to-use-scripts); specifically, one of the recommendations was to use scripts whenever you need to run a program multiple times.  So let's try writing a script called increment.py that solves our problem.  Here's the script:

```python
my_favorite_number = 941
print(my_favorite_number + 1)
```

And here's the output it produces

```shell
$ python increment.py
942
```

This is easy to rerun, but we still haven't resolved this issue where we can't change your favorite number without rewriting the code.  And now is when the magic of the `input` function comes in handy.  

> The **input** function allows a user to input data into a program.

Let's see it in action.  Try out the following script:

```python
my_favorite_number = input("Enter your favorite number: ")
print(int(my_favorite_number) + 1)
```

Compared to the last version of increment.py, two things have changed.  In the first line, we used the input command to ask the user to input a number.  And the second line is almost the same, but to make sure the addition works correctly, we need to convert the number you input from a string to an integer, and hence the use of the `int` function (I'll say more about this in the next lesson on [variables]({{< ref "/python/variables.md" >}} "Variables")).  Now, when you run your program, you'll be able to enter your favorite number:

```shell
$ python increment.py 
Enter your favorite number: 1995
1996
```

And there you have it!  We've solved our problem.

---

#### Exercise 3 (Using the input function)

The input function is a powerful friend.  It accepts all kinds of things.  In this exercise, we're going to stretch the limits of what the input function can do.

For starters, write a program called my_sum.py which accepts not one, but two inputs.  It should prompt the user for two different numbers, and then return their sum.  Here's the kind of output I'm looking for:

```shell
$ python my_sum.py
Enter your first number: 14
Enter your second number: 7
21
```

---

#### Exercise 4 (More practice with the input function)

Next, create a Python script called just_checking_in.py.  This script is all about self-care.  I want you to ask yourself a question, and then supply the answer.  Your program should start by asking you to input a question.

```shell
$ python just_checking_in.py
Type a question:
```

I want to self-evaluate a little, so I'll ask myself how I'm doing:

```shell
$ python just_checking_in.py
Type a question: How are you doing? 
```

Your program should then ask you the question you typed in.  Here's what it should look like end-to-end:

```shell
$ python increment.py 
Type a question: How are you doing? 
How are you doing? I am finding my own happiness.
```

For a bonus point, can you write this script in one line of Python?

---

### Review

Let's summarize what we've learned in this lesson.

* [Interacting with Python](#interacting-with-python).  There are two main ways of interacting with Python: shells and scripts.

    * [Python shell](#python-shell).  The Python **shell** is an interpreter that allows you to execute Python commands one by one.

    * [Python scripts](#python-scripts).  A Python **script** is a file containing Python code that can be executed from the command line.

* [When to use the shell and when to use scripts](#when-to-use-the-shell-and-when-to-use-scripts).  The shell is best for executing simple Python commands.  For long and/or more complicated programs, it's often easier to use a script (or multiple scripts) instead of a shell.

* [Print statements](#print-statements).  The **print** function allows you to print output to the console.  This is one of the most used commands in Python.

* [Exercise 1 (From the shell to a script)](#exercise-1-from-the-shell-to-a-script).  

* [Exercise 2: Your first Python program](#exercise-2-your-first-python-program)

* [User-supplied input](#user-supplied-input).  The **input** function allows a user to input data into a Python program.

* [Exercise 3 (Using the input function)](#exercise-3-using-the-input-function)

* [Exercise 4 (More practice with the input function)](#exercise-4-more-practice-with-the-input-function)

---

Great work!  you made it through the first lesson.  Next up is a lesson about Python [variables]({{< ref "/python/variables.md" >}} "Variables").  Looking forward to seeing you there!