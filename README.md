# Hidralpress Backend

Este projeto tem como objetivo automatizar o registro fotográfico para a empresa Hidralpress. As fotos tiradas por sua equipe são organizadas e salvas automaticamente na pasta correta no computador, de acordo com a ordem de serviço (OS) e o setor (montagem ou desmontagem).

## Tecnologias Utilizadas

- **Django**: Framework web utilizado para desenvolver o backend da aplicação.
- **Django Storage**: Utilizado para gerenciar o armazenamento dos arquivos de imagem.
- **Docker**: Contêineres Docker são usados para facilitar o desenvolvimento, a implantação e a execução do aplicativo em diferentes ambientes.

## Funcionalidades

- **Automação do Registro Fotográfico**: As fotos são associadas automaticamente às etapas específicas dentro dos setores e, no final, relacionadas a uma OS.
- **Organização de Arquivos**: As imagens são salvas em pastas específicas com base na OS e no setor, garantindo uma estrutura de armazenamento eficiente e organizada.
- **Integração com Docker**: Facilita a configuração e o gerenciamento do ambiente de desenvolvimento e produção.

## Como Executar

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/hidralpress-backend.git
    ```

2. Navegue até o diretório do projeto:
    ```sh
    cd hidralpress-backend
    ```

3. Use o Docker Compose para criar e iniciar os contêineres:
    ```sh
    docker-compose up
    ```

4. Acesse a aplicação:
    - Acesse o endereço `http://localhost:8000` no seu navegador para ver a aplicação em funcionamento.

