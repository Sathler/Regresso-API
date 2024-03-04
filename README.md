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
