# AppContagem

## Descrição

O Aplicativo de Contagem de Códigos de Barras é uma ferramenta para auxiliar na contagem de itens por meio de códigos de barras. Ele permite criar novas contagens, adicionar setores, bipar códigos de barras, visualizar resumo da contagem e realizar download dos dados.

## Tecnologias Usadas

- **Python**: Linguagem de programação utilizada para desenvolver a lógica do aplicativo.
- **Tkinter**: Biblioteca gráfica utilizada para criar a interface do usuário.
- **SQLite3**: Banco de dados embutido utilizado para armazenar os dados das contagens e códigos de barras.

## Funcionalidades

- Criar uma nova contagem.
- Adicionar e gerenciar setores dentro de uma contagem.
- Bipar códigos de barras e registrar se foram encontrados ou não em um setor.
- Excluir códigos de barras.
- Finalizar um setor ou uma contagem.
- Visualizar um resumo da contagem com estatísticas.

## Configuração e Execução

### Pré-requisitos

- Python instalado na máquina.

### Instalação e Execução

1. Clone o repositório do GitHub para sua máquina local:

git clone https://github.com/leandrotobita/appcontagem.git

2. Navegue até o diretório do projeto:

cd appcontagem

3. Execute CriarCodigoBarrasDB.py para criar o codigobarras.db (dados dos produtos)

phyton CriarCodigoBarrasDB.py

3. Execute o aplicativo Python:

python AppContagem.py

Isso iniciará o aplicativo de contagem de códigos de barras.


### Telas

<img src="screenshots/TelaInicial.png">
Tela Inicial

<img src="screenshots/encontrado.png">
Resultado de um código encontrado

<img src="screenshots/final.png" alt="Tela Inicial" width="400">
Resumo da contagem com a possibilidade de download em formato .txt




