Do not use defensive programming, but appropriate type declarations are encouraged. 
For example: clearly defining parameter types and return values in function signatures to improve readability, rather than adding redundant runtime checks or excessive null guards for every variable. 

✅ **Good (Appropriate Type Declaration):**
```python
def add(a: float, b: float) -> float:
    return a + b
```

❌ **Bad (Defensive Programming):**
```python
def add(a, b):
    if not isinstance(a, (int, float)):
        raise TypeError("First argument must be a number")
    if not isinstance(b, (int, float)):
        raise TypeError("Second argument must be a number")
    # ... lots of other runtime validations
    return a + b
```