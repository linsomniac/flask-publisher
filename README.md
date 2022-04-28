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

The 
