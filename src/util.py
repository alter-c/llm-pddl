def postprocess(x: str) -> str:
    return x.strip().replace("```",'').replace("pddl",'').replace("lisp",'')

def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
                if result:
                    break
            return result
        return wrapper
    return decorator