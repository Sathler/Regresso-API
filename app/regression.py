from scipy.optimize import curve_fit
import numpy as np
from app.custom_interpreter import custom_interpreter, create_function
import re

class Regression():
    def __init__(self, type = None) -> None:
        self.type = type

    def linear_function(self, x, a, b):
        return a*x + b

    def quadratic_function(self, x, a, b, c):
        return a * (x ** 2) + b * x + c 
    
    def cubic_function(self, x, a, b, c, d):
        return a * (x ** 3) + b * (x ** 2) + c * x + d
    
    def exp_function(self, x, a, b):
        return a * (b**x)
    
    def logaritmic_function(self, x, a, b):
        return a * np.log2(x) + b
    
    def n_logaritmic_function(self, x, a, b):
        return a * x * np.log2(x) + b

    def n2_logaritmic_function(self, x, a, b):
        return a * (x ** 2) * np.log2(x) + b
    
    def power_function(self, x, a, b):
        return a * (x ** b)
    
    def ema_function(self, x, a, b, c, d ,e, f):
        return a * (b ** (x ** c)) * (x ** d) * (np.log2(x) ** e) + f
    
    def n_logaritmic2_function(self, x, a, b):
        return a * x * (np.log2(x) ** 2) + b
    
    def regression(self, x_values, y_values, aprox = 2, expr = None, maxfev=10000):
        functions = {
            'linear': self.linear_function,
            'quadratic': self.quadratic_function,
            'cubic': self.cubic_function,
            'exp': self.exp_function,
            'logaritmic': self.logaritmic_function,
            'n_logaritmic': self.n_logaritmic_function,
            'n2_logaritmic': self.n2_logaritmic_function,
            'n_logaritmic2': self.n_logaritmic2_function,
            'ema': self.ema_function,
            'power': self.power_function,
            'custom': lambda x: x,
        }

        if self.type == 'custom':
            if not expr:
                raise Exception("O calculo de uma expressao customizada exige a expressao a ser avaliada")

            custom_function, free_variables = custom_interpreter(expr)

            function = create_function(custom_function)

        else:
            function = functions.get(self.type)

        if not function:
            raise Exception(f'Tipo de regressão {self.type} não encontrado')
        
        x_data = np.array(x_values, dtype=np.float64)
        y_data = np.array(y_values, dtype=np.float64)
        
        info = curve_fit(function, x_data, y_data, maxfev=maxfev, full_output=True)
        params = info[0]
        print(f"Foram necessarias {info[2]['nfev']} iterações para chegar ao resultado")

        if self.type == 'custom':
            words = re.findall(r'\b\_?[a-zA-Z]+\d*\b', expr)

            params_variables = {free_variables[i]: f"{params[i]:.{aprox}f}" for i in range(len(params))}

            expr_interpretada = re.sub(r'\b\_?[a-zA-Z]+\d*\b', lambda x: params_variables.get(x.group(0), x.group(0)), expr)

        result = list(map(lambda x: np.round(x, aprox),params))

        #calculando valores de y ajustados
        y_fit = function(x_data, *params)

        #calculando erro relativo médio
        relative_error = np.mean(np.abs((y_fit - y_data) / y_data))

        #calculando coeficiente de determinação
        mean_y = np.mean(y_data)
        total_sum_of_squares = np.sum((y_data - mean_y)**2)
        sum_of_squared_residuals = np.sum((y_data - y_fit)**2)
        r_squared = 1 - (sum_of_squared_residuals / total_sum_of_squares)

        #calculando coeficiente de correlação
        correlation_coefficient = np.corrcoef(y_data, y_fit)[0, 1]

        response = {f'coef_{i}': x for i, x in enumerate(result)}
        response['relative_error'] = relative_error
        response['r_squared'] = r_squared
        response['correlation_coefficient'] = correlation_coefficient
        if self.type == 'custom':
            response['expression'] = expr_interpretada

        if self.type == 'custom':
            x1 = min(x_values)
            x2 = max(x_values)
            delta = max((x2 - x1)/100.0, 0.1)
            x_points = [np.round(x, 4) for x in np.arange(x1, x2+(delta/2), delta)]
            y_points = [np.round(function(x, *params), 4) for x in x_points]

            response['x_points'] = x_points
            response['y_points'] = y_points

            return response

        return response