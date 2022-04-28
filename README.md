# Flask-Publisher

## Overview

This is a decorator for Flask functions to automatically bring GET/POST arguments
to the function via argument inspection and optionally type annotations.

This is modeled on the mod\_python Publisher handler.

## Example

```python
from publisher import publish

@app.route('/register')
@publish()
def register(full_name, email, age:int=None):
    return f'Registered {full_name} at e-mail address {email} and they are {age} years old'
```

## Details

The function arguments are inspected and used to extract the values from the request
GET/POST data (via request.values).  If type annotations are specified, the incoming
values will be instantiated as that type.  If "\*\*kwargs" is included, remaining GET/POST
values are placed there, otherwise they are ignored.

## Why?

I understand the arguments for using path-based arguments.

In my case, we had existing code using mod\_python Publisher semantics that we wanted to
port to Python3 and Flask, making as few changes to the other parts of the code as possible.

## Inspiration

This was inspired by the answer at https://stackoverflow.com/a/34597794
and the type annotation magic of FastAPI and Typer.
