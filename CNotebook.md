# Python Related

Since Python is a **scripting language**, it does not typically indicate if the program has bugs at first. If the program falls into an **infinite loop**, there is no warning or suggestion from the interpreter. Instead, the program will run **indefinitely** without producing an output, which means we can't see when it finishes.

To **diagnose what went wrong**, it is often suggested to have the program **output the values of its variables**. Additionally, **using debugging tools** can be very helpful.

### Difference Between Docstring and Triple Double-Quoted String

In Python, `docstring` and `triple double-quoted string` are essentially the same syntactically, but they serve different purposes depending on the context.

#### 1. Triple Double-Quoted String (`"""`)
- It is a syntax in Python used to define multi-line strings. It can be used as a `docstring` or as a regular string.
- It allows you to include multiple lines of text, supporting line breaks and special characters, similar to single-line strings but better suited for long texts.

Example:
```python
s = """This is a multi-line
string that spans multiple
lines."""
```

#### 2. Docstring

A docstring is a special type of multi-line string (usually defined with """ or ''') used to provide documentation for modules, classes, methods, or functions. It must appear as the first line in the definition.
Python stores the docstring as the __doc__ attribute of the object, which can be accessed via help() or directly through __doc__.
Example:


```python
def my_function():
  """
  This is a docstring for my_function.
  It explains what the function does.
  """
  pass

  print(my_function.__doc__)  # Outputs the docstring
```

**Key Differences:**
`Docstring` serves a special purpose as documentation and is associated with Python objects.
Triple double-quoted string is just a syntax for writing multi-line strings and can be used for any general text.
In summary, a docstring is a specific use case of a triple-quoted string, mainly for writing documentation, while a triple-quoted string can be used anywhere you need multi-line text.
