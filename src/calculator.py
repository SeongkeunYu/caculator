import copy


class Calculator:
    def __init__(self):
        self._history = []

    def _validate(self, *args):
        for value in args:
            if not isinstance(value, (int, float)):
                raise TypeError(f"Unsupported type: {type(value)}")

    def _record(self, operation, operands, result):
        self._history.append({"operation": operation, "operands": operands, "result": result})

    def add(self, a, b):
        self._validate(a, b)
        result = a + b
        self._record("add", [a, b], result)
        return result

    def subtract(self, a, b):
        self._validate(a, b)
        result = a - b
        self._record("subtract", [a, b], result)
        return result

    def multiply(self, a, b):
        self._validate(a, b)
        result = a * b
        self._record("multiply", [a, b], result)
        return result

    def divide(self, a, b):
        self._validate(a, b)
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        result = a / b
        self._record("divide", [a, b], result)
        return result

    def get_history(self):
        return copy.deepcopy(self._history)

    def clear_history(self):
        self._history = []

    def reset(self):
        self._history = []
