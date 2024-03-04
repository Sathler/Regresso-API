import re
import math
import numpy as np

def custom_interpreter(expression: str):
    reserved_words = {
        '_e', '_pi', 'loge', 'log10', 'log2'
    }

    equivalent_expr = {
        'log2': 'np.log2',
        'log10': 'np.log10',
        'log2': 'np.log',
        '_e': 'math.e',
        '_pi': 'math.pi',
    }

    words = re.findall(r'\b\_?[a-zA-Z]+\d*\b', expression)

    if 'x' not in words:
        raise Exception("Variável livre x obrigatória na expressão")

    invalid_names =  any(
        [len(x) > 1 and not x in reserved_words for x in words]
    )

    if invalid_names:
        raise Exception("Expressao customizada possui termos inválidos.")
    
    free_variables = [x for x in words if len(x) == 1 and x != 'x']

    for key, value in equivalent_expr.items():
        expression = expression.replace(key, value)

    return f"""
def my_custom_function(x{',' + ','.join(free_variables)}):
    return {expression}""", free_variables

def create_function(expression: str):
    exec(expression, globals())
    return my_custom_function