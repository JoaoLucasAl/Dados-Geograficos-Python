# Dados-Geograficos-Python
Usuários de um determinado nicho, para descrever locais de interesse em uma área geográfica, tem a necessidade de armazenar pontos geográficos (latitude e longitude) com uma descrição (Ex. escola, farmácia). Para tal aplicação um backend é necessário. Desenvolva um backend em python que permita o cadastro, visualização, alteração e remoção de usuários e pontos geográficos. Os dados devem ser armazenados em um banco de dados MongoDB.


# Para que a API funcione instale os pacotes:
``` python
pip install fastapi
pip install uvicorn[standard]
pip install pymongo
pip install pytest
pip install requests
pip install email-validator
```

E rode o seguinte comando:
``` python
uvicorn main:app --reload
```

# Documentação
Durante a execução do programa acesse o endereço disponibilizado após executar o comando do uvicorn + /docs

# Testes Unitarios
Os testes unitarios devem ser feitos antes da API ser de fato usada ou em um banco de dados vazio!
