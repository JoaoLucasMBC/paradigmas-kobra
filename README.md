# Linguagem Kobra

## Desenvolvedores
- [João Lucas de Moraes Barros Cadorniga](https://github.com/JoaoLucasMBC)
- [Eduardo Mendes Vaz](https://github.com/EduardoMVAz)

## Funcionamento e Documentação

todo: gramática

Nesse repositório está o código para a linguagem Kobra. Para utilizar a linguagem, clone o repositório na sua máquina:
        git clone https://github.com/JoaoLucasMBC/paradigmas-kobra.git

Crie um ambiente virtual na pasta do projeto:

    windows:
        python -m venv env
    linux:
        python3 -m venv env

E instale todas as dependências do projeto, presentes em `requirements.txt`:

        pip install -r requirements.txt

No notebook `kobra.ipynb`, está a linguagem está dividida em paradigmas demonstrando o processo de desenvolvimento, com exemplos.

Já o arquivo `kobra.py` é como um "compilador" da linguagem. Você pode usar esse arquivo para rodar códigos escritos em Kobra. Para fazer isso, você deve criar um arquivo de texto na pasta do repositório, **que contenha um código Kobra válido** (para entender como usar a linguagem, consulte a gramática acima ou um dos exemplos `.kbr` presentes no repositório) e então executar o seguinte comando:

    windows:
        python kobra.py nome-do-arquivo-aqui.extensão-do-arquivo
    linux:
        python3 kobra.py nome-do-arquivo-aqui.extensão-do-arquivo

O executor irá então imprimir no terminal o resultado da execução do arquivo. Para o exemplo `in02.kbr`, a saída no terminal seria:

![in02](assets/kobra.png)

Sendo que os prints em abaixo de "RUNTIME" representam as coisas impressas durante a execução do código Kobra, e o "Result" representa o **estado final das variáveis criadas no código**.

## Dependências e Funcionalidades

A linguagem Kobra foi desenvolvida usando Python como base e usando a biblioteca rply.