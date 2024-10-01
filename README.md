# Regresso-API

Módulo da aplicação Regresso responsável pelo cálculo do ajuste de curvas, este documento deve guiar um usuário a instanciar uma api localmente usando o FastAPI. Atente-se que este guia foi criado e testadop em uma máquina windows e usando Python na versão 3.9

## Passo 1: Criar um ambiente virtual para Python

Na raiz do projeto rode o código

```cmd
python -m venv venv
```

Isso irá gerar uma pasta na raiz chamada `venv`. Você pode modificar este nome mudando o ultimo parâmetro da instrução acima

## Passo 2: Ativar o Ambiente Virtual

Depois de criar o ambiente virtual, você precisa ativá-lo. Dependendo do sistema operacional, o comando pode variar:
- No Windows:
  ```bash
  venv\Scripts\activate.bat
  ```
- No Linux/macOS:
  ```bash
  source venv/bin/activate
  ```

Outro ponto a se atentar é que o terminal também pode mudar o arquivo a ser executado. O arquivo com terminação `bat` é executado no prompt de comando do Windows `cmd`.

## Passo 3: Instalar Pacotes a partir de requirements.txt

Com o ambiente virtual ativado, você pode instalar os pacotes listados no arquivo requirements.txt usando o pip:
```bash
pip install -r requirements.txt
```
Isso instalará todos os pacotes especificados no arquivo requirements.txt no seu ambiente virtual.

Observe que todos os passos até aqui podem diferir de ambiente para ambiente, em caso de dúvidas procure guias sobre como iniciar um ambiente virtual e instalar dependências em python para um ambiente compatível com o seu.

## Passo 4: Hospedar a API localmente

Com o ambiente virtual criado e as dependências instaladas já é possível hospedar a API.

execute o seguinte código na raiz do projeto.

```cmd
uvicorn api:app --reload
```

dessa maneira a API local será disponibilizada no endereço `http://127.0.0.1:8000`, você pode usar softwares terceiros como o Postman para testar.

## Parâmetros da Regresso-API

### Parâmetros da Requisição (POST)

- **type** (`string`): Define a curva a ser ajustada. Pode ser um dos seguintes valores:
  - `linear`: $f(x) = a*x + b$
  - `quadratic`: $f(x) = a * x^2 + b*x + c$
  - `cubic`: $f(x) = a * x^3 + b * x^2 + c*x + d$
  - `exp`: $f(x) = a * b^x$
  - `logaritmic`: $f(x) = a*\log_2(x) + b$
  - `n_logaritmic`: $f(x) = a * x * \log_2(x) + b$
  - `n2_logaritmic`: $f(x) = a * x^2 *\log_2(x) + b$
  - `n_logaritmic2`: $f(x) = a * x * \log_2(x)^2 + b$
  - `ema`: $f(x) = a * b^{x^c} * x^d *\log_2(x)^e + f$
  - `power`: $f(x) = a*x^b$
  - `custom`: Curva definida pela expressão no parâmetro `expr`

- **params** (`array`): Valores das variáveis independentes para o ajuste (eixo X).

- **results** (`array`): Valores das variáveis dependentes para o ajuste (eixo Y).

- **aprox** (`int`, opcional): Precisão decimal desejada. Padrão: 4.

- **maxfev** (`int`, opcional): Número máximo de iterações do Algoritmo de Levenberg-Marquardt (máximo: 10.000).

- **expr** (`string`, opcional): Expressão da curva, usada apenas se o tipo for `custom`.

- **print_aprox** (`int`, opcional): Precisão decimal para a expressão ajustada. Relevante apenas se o tipo for `custom`.

### Exemplo de Requisição

```json
{
  "type": "quadratic",
  "params": [1, 2, 3, 4, 5],
  "results": [1, 4.3, 8.25, 16.7, 23.22],
  "aprox": 4
}
```

### Parâmetros da Resposta da API

- **success** (`boolean`): Indica se a execução da requisição foi bem-sucedida (`true`) ou se houve um erro (`false`).

- **message** (`string`, opcional): Mensagem explicativa em caso de falha na execução da requisição.

- **response** (`object`): Dicionário com os resultados do ajuste da curva, contendo os seguintes campos:
  - **coef_0**, **coef_1**, ... (`float`): Coeficientes calculados para o ajuste da curva. O número de coeficientes depende do tipo de ajuste.
  - **relative_error** (`float`): Erro relativo médio do ajuste, indicando a precisão da regressão.
  - **r_squared** (`float`): Coeficiente de determinação ($R^2$), que mede a qualidade do ajuste.
  - **correlation_coefficient** (`float`): Coeficiente de correlação de Pearson ($\rho$), que indica a força da correlação entre as variáveis.
  - **rmse** (`float`): Raiz quadrada do erro médio quadrático (RMSE), que é uma métrica de erro do ajuste.
  - **expression** (`string`, opcional): Expressão da curva ajustada com os coeficientes calculados. Retornado apenas se o tipo for `custom`.
  - **x_points** (`array`, opcional): Sequência de valores gerados para as variáveis independentes (eixo X). Retornado apenas se o tipo for `custom`.
  - **y_points** (`array`, opcional): Sequência de valores gerados para as variáveis dependentes (eixo Y) com base no ajuste da curva. Retornado apenas se o tipo for `custom`.


### Exemplo de retorno

```json
{
    "success": true,
    "response": {
        "coef_0": 0.7814,
        "coef_1": 0.9954,
        "coef_2": -0.888,
        "relative_error": 0.06361372457326672,
        "r_squared": 0.9934831824361064,
        "correlation_coefficient": 0.9967362652357478,
        "rmse": 0.659595547069783
    }
}
```

### Restrições para os Coeficientes nos Ajustes de Curva

| Tipo de Ajuste        | Equação da Curva                             | Restrição            |
|-----------------------|----------------------------------------------|----------------------|
| Linear                | $f(x) = a*x + b$                             | $a >= 0.01$ ou $a <= -0.01$ |
| Quadrático            | $f(x) = a * x^2 + b*x + c$                     | $a >= 0.01$ ou $a <= -0.01$ |
| Cúbico                | $f(x) = a * x^3 + b * x^2 + c*x + d$             | $a >= 0.01$ ou $a <= -0.01$ |
| Logarítmico           | $f(x) = a*\log_2(x) + b$                     | $a >= 0.01$ ou $a <= -0.01$ |
| $N\log_2(N)$          | $f(x) = a * x * \log_2(x) + b$                   | $a >= 0.01$ ou $a <= -0.01$ |
| $N\log_2(N)^2$        | $f(x) = a * x * \log_2(x)^2 + b$                 | $a >= 0.01$ ou $a <= -0.01$ |
| $N^2\log_2(N)$        | $f(x) = a * x^2 * \log_2(x) + b$                 | $a >= 0.01$ ou $a <= -0.01$ |
| Potência              | $f(x) = a*x^b$                               | $b >= 1.1$ ou $b <= 0.9$    |

### Regressão Personalizada

Para que a função seja considerada válida, ela deve seguir um conjunto de regras estabelecidas para evitar vulnerabilidades de segurança, como a injeção de código.

Entre as restrições impostas, destaca-se que nenhum argumento da função pode conter mais de um caractere, exceto em casos específicos, que estão listados a seguir:

- **log**: Equivale à função logarítmica na base natural.
- **log2**: Equivale à função logarítmica na base dois.
- **log10**: Equivale à função logarítmica na base dez.
- **exp**: Equivale à função exponencial \(e^x\).
- **sin**: Equivale à função seno.
- **sen**: Alternativa em português à função seno.
- **cos**: Equivale à função cosseno.
- **tan**: Equivale à função tangente.
- **sqrt**: Equivale à função raiz quadrada.
- **abs**: Equivale à função absoluta.
- **floor**: Retorna a parte inteira do seu parâmetro.
- **ceil**: Retorna o menor número inteiro maior do que o seu parâmetro.
- **_e**: Equivale ao número de Euler (\(e\)).
- **_pi**: Equivale à constante \(\pi\).

As funções acima são aquelas consideradas para a aproximação customizada, operadores aritméticos podem ser escritos de maneira semelhante a aceita pela linguagem python.