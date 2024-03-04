from app.regression import Regression
import os

def regression_handler(event, context):
    print("Iniciando processamento")
    print(event)

    try:
        body = event.get('body-json')
        
        if not body:
            raise Exception("Corpo da requisição vazio")
        
        type_param = body.get("type")
        params = body.get("params")
        results = body.get("results")
        aprox = body.get('aprox', 4)
        expr = body.get('expr', 4)
        maxfev = body.get('maxfev', 10000)

        limite_maxfev = os.getenv('MAXFEV')

        if limite_maxfev is not None:
            if maxfev > int(limite_maxfev):
                raise Exception(f"Limite máximo de iterações não pode ser superior á {limite_maxfev}")

        if not params:
            raise Exception("Parametro 'params' obrigatório")
        
        if not results:
            raise Exception("Parametro 'result' obrigatório")
        
        if not type_param:
            raise Exception("Parametro 'type' obrigatório")
        
        if not isinstance(params, list):
            raise Exception("Parametros 'params' deve ser lista")
        
        if not isinstance(results, list):
            raise Exception("Parametros 'results' deve ser lista")
        
        if len(params) != len(results):
            raise Exception("Tamanho de params e results devem ser iguais")
        
        if len(params) > 100:
            raise Exception("Não são aceitos mais de 1000 parametros")
        
        reg = Regression(type_param)

        return {
            "success": True,
            "response": reg.regression(params, results, aprox, expr=expr, maxfev=maxfev)
        }

    except Exception as error:
        raise error
        print("Erro no processamento")
        print(str(error))
        return {
            'success': False,
            'message': str(error)
        }
