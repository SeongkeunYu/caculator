import sys
import os
import math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from calculator import Calculator

OPERATORS = {"+": "add", "-": "subtract", "*": "multiply", "/": "divide"}

def parse(expr):
    for op in ("*", "/", "+", "-"):
        parts = expr.split(op, 1)
        if len(parts) == 2:
            left, right = parts[0].strip(), parts[1].strip()
            try:
                return float(left) if "." in left else int(left), op, float(right) if "." in right else int(right)
            except ValueError:
                return None
    return None

def fmt(value):
    if isinstance(value, float):
        if not math.isfinite(value):
            return value
        if value == int(value):
            return int(value)
    return value

def man():
    print("  Commands:")
    print("    <a> + <b>   addition")
    print("    <a> - <b>   subtraction")
    print("    <a> * <b>   multiplication")
    print("    <a> / <b>   division")
    print("    history     show operation history")
    print("    reset       reset calculator (clears history)")
    print("    man         show this help")
    print("    quit        exit program")

def main():
    calc = Calculator()
    print("=== Calculator ===")
    man()
    print()

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue

        if line == "quit":
            break

        if line == "history":
            history = calc.get_history()
            if not history:
                print("  (empty)")
            for h in history:
                op_sym = next((s for s, n in OPERATORS.items() if n == h["operation"]), "?")
                a, b = h["operands"]
                print(f"  {a} {op_sym} {b} = {fmt(h['result'])}")
            continue

        if line == "man":
            man()
            continue

        if line == "reset":
            calc.reset()
            print("  history cleared")
            continue

        parsed = parse(line)
        if parsed is None:
            print("  invalid expression  (example: 3 + 5)")
            continue

        a, op, b = parsed
        try:
            method = getattr(calc, OPERATORS[op])
            print(f"  {fmt(method(a, b))}")
        except ZeroDivisionError:
            print("  error: division by zero")
        except OverflowError:
            print("  error: result out of range")
        except TypeError as e:
            print(f"  error: {e}")

if __name__ == "__main__":
    main()
