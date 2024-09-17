from .text import *

# DSL context initialization
dsl_context = {
    'contains': contains,
    'to_lower': to_lower,
    'rand_base': rand_base,
}

def evaluate_dsl(expression):
    try:
        # Hanya izinkan evaluasi berdasarkan fungsi yang diizinkan
        if not isinstance(expression, str):
            raise ValueError("Expression must be a string.")
        # Evaluasi ekspresi dengan menggunakan fungsi yang diizinkan
        result = eval(expression, {"__builtins__": None}, dsl_context)
        if result is None:
            raise ValueError(f"Evaluation result is None for expression: {expression}")
        return result
    except Exception as e:
        raise ValueError(f"Error evaluating DSL: {e}")
