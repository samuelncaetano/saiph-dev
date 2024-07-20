# Saiph

## Configurar Ambiente Virtual

Para evitar conflitos de dependências e garantir que todas as bibliotecas necessárias estejam instaladas corretamente, configure um ambiente virtual:

1. Instalar o virtualenv se ainda não estiver instalado:

```bash
pip3 install virtualenv
```

2. Criar um novo ambiente virtual:

```bash
virtualenv -p python3 .venv
```

3. Ativar o ambiente virtual:

```bash
source .venv/bin/activate
```

## Instalar Dependências

Com o ambiente virtual ativado, instale todas as dependências necessárias para o projeto:

```bash
pip3 install -r requirements.txt
```

```bash
pip3 install pydantic black pylint flake8 pyright pytest coverage pre-commit commitizen
```
