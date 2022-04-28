#!/usr/bin/env python3
#
#  Flask-Publisher
#  https://github.com/linsomniac/flask-publisher
#  Sean Reifschneider, April 2022
#  License: CC0 1.0 Universal

from functools import wraps
from flask import request
import inspect


def publish():
    """Decorator the publishes the Flask function, wiring up arguments to the incoming request.

    The function arguments are inspected and used to extract the values from the request
    GET/POST data (via request.values).  If type annotations are specified, the incoming
    values will be instantiated as that type.  If "**kwargs" is included, remaining GET/POST
    values are placed there, otherwise they are ignored.

    Example:

    @app.route("/somewhere")
    @publish()
    def somewhere(gender:str, age:int=None):
        return jsonify(gender=gender, age=age)
    """

    def decorator(f):
        def _is_var_kw(signature: inspect.Signature) -> bool:
            """Is the signature one with a "variable keyword args" (**kwargs)

            Args:
                signature: Function signature.

            Returns:
                True if the signature includes a "**kwargs".
            """
            for x in signature.parameters.values():
                if x.kind == 4:
                    return True
            return False

        def _extract_args() -> dict:
            """Extract the request.values (GET/POST data) into a dictionary suitable for passing
            to the wrapped function as **kwargs.

            Returns:
                A dictionary of kwargs to pass to the wrapped function.
            """
            results = {}

            for key in request.values.keys():
                if key in f_signature.parameters:
                    annotation = f_signature.parameters[key].annotation
                    if annotation != inspect._empty:
                        results[key] = request.values.get(key=key, type=annotation)
                    else:
                        results[key] = request.values.get(key=key)

                elif map_all_params:
                    results[key] = request.values.get(key=key)

            return results

        f_signature = inspect.signature(f)
        map_all_params = _is_var_kw(f_signature)

        @wraps(f)
        def wrapper(*_, **kwargs):
            final_kwargs = _extract_args()
            return f(**final_kwargs)

        return wrapper

    return decorator
