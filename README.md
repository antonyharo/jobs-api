## Instalar dependências

```
git clone https://github.com/AntonyHaro/jobs-api.git
```

```
cd jobs-api
```

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
pip install -r requirements.txt
```

## Rodar scripts de teste:

Para verificar se a lib jobspy está funcionando corretamente:

```
python tests/test_jobspy.py
```

## Iniciar API:

```
python app.py
```

Para verificar se a API de busca de vagas está funcionando corretamente (a API deve estar rodando antes de executar este comando!):

```
python tests/test_api.py
```

