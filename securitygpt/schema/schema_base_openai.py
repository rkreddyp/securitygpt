from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json
from functools import wraps
from typing import Any, Callable
from pydantic import validate_arguments, BaseModel

## openai_schema
class OpenAISchema(BaseModel):
    @classmethod
    @property
    def openai_schema(cls):
        schema = cls.schema()
        parameters = {
            k: v for k, v in schema.items() if k not in ("title", "description")
        }
        parameters["required"] = sorted(parameters["properties"])
        #_remove_a_key(parameters, "title")
        return {
            "name": schema["title"],
            "description": schema["description"],
            "parameters": parameters,
        }

    @classmethod
    def from_response(cls, completion, throw_error=True):
        message = completion.choices[0].message

        if throw_error:
            assert "function_call" in message, "No function call detected"
            assert (
                message["function_call"]["name"] == cls.openai_schema["name"]
            ), "Function name does not match"

        function_call = message["function_call"]
        arguments = json.loads(function_call["arguments"])
        return cls(**arguments)

## class openai_function_schema

class openai_function:
    
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.validate_func = validate_arguments(func)
        parameters = self.validate_func.model.schema()
        parameters["properties"] = {
            k: v
            for k, v in parameters["properties"].items()
            if k not in ("v__duplicate_kwargs", "args", "kwargs")
        }
        parameters["required"] = sorted(
            parameters["properties"]
        )  # bug workaround see lc
        _remove_a_key(parameters, "title")
        _remove_a_key(parameters, "additionalProperties")
        self.openai_schema = {
            "name": self.func.__name__,
            "description": self.func.__doc__,
            "parameters": parameters,
        }
        self.model = self.validate_func.model

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        @wraps(self.func)
        def wrapper(*args, **kwargs):
            return self.validate_func(*args, **kwargs)

        return wrapper(*args, **kwargs)

    def from_response(self, completion, throw_error=True):
        """Execute the function from the response of an openai chat completion"""
        message = completion.choices[0].message

        if throw_error:
            assert "function_call" in message, "No function call detected"
            assert (
                message["function_call"]["name"] == self.openai_schema["name"]
            ), "Function name does not match"

        function_call = message["function_call"]
        arguments = json.loads(function_call["arguments"])
        return self.validate_func(**arguments)

    def openai_schema(cls):
        schema = cls.schema()
        parameters = {
            k: v for k, v in schema.items() if k not in ("title", "description")
        }
        parameters["required"] = sorted(parameters["properties"])
        
        return {
            "name": schema["title"],
            #"description": schema["description"],
            "parameters": parameters,
        }