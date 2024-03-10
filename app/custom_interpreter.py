import re
import math
import numpy as np

def custom_interpreter(expression: str):
    reserved_words = {
        '_e', '_pi', 'loge', 'log10', 'log2'
    }

    equivalent_expr = {
        'log': 'np.log',
        'log2': 'np.log2',
        'log10': 'np.log10',
        '_e': 'math.e',
        '_pi': 'math.pi',
        'exp': 'np.exp',
        'sin': 'np.sin',
        'sen': 'np.sin',
        'cos': 'np.cos',
        'tan': 'np.tan',
        'sqrt': 'np.sqrt',
        'abs': 'np.abs',
        'floor': 'np.floor',
        'ceil': 'np.ceil',
    }

    reserved_words = set(equivalent_expr.keys())

    words = re.findall(r'\b\_?[a-zA-Z]+\d*\b', expression)

    if 'x' not in words:
        raise Exception("Variável livre x obrigatória na expressão")

    invalid_names =  any(
        [len(x) > 1 and not x in reserved_words for x in words]
    )

    if invalid_names:
        raise Exception("Expressao customizada possui termos inválidos.")
    
    free_variables = [x for x in words if len(x) == 1 and x != 'x']

    for word in words:
        if word in equivalent_expr:
            expression = expression.replace(word, equivalent_expr[word])

    return f"""
def my_custom_function(x{',' + ','.join(free_variables)}):
    return {expression}""", free_variables

def create_function(expression: str):
    exec(expression, globals())
    return my_custom_function