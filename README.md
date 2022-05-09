# FollowPhone - Projeto Final CS50X 2020

![Mockup](static/img/followphone_mockup.png)  

Essa aplicação web te ajuda a acompanhar a conversa que você tem com qualquer um, sendo eles parceiros de negócios ou seus amigos.

Veja a [aplicação](https://followphone.herokuapp.com/) em primeira mão!

## Aviso para estudantes do CS50

Conforme as diretrizes de [Academic Honesty](https://cs50.harvard.edu/x/2022/honesty/) (Honestidade Acadêmica), você **não está permitido** de basear seus projetos neste. O objetivo desse repositório é mostrar as habilidades que aprendi durante o curso do CS50 para fins profissionais e empregadores futuros. Assim assumo que:

- Você já tenha terminado o curso para estar aqui.
- Caso contrário, não acesse qualquer conteúdo deste repositório.
- Eu não me responsabilizo por como você usa este repositório.

Este repositório e seu conteúdo não deve ser compartilhado sem a autorização do autor para alunos do CS50 ou para aqueles que farão o curso no futuro. Mais uma vez peço que aja com honestidade e ética, em especial se você for aluno do CS50 ou pretende cursá-lo futuramente.

## Como usar

- Crie uma **conta**
- Adicione quantos **contacts** você quiser
- Acompanhe qualquer conversa / negócio que tiver com eles por criar **histories**
- Você pode adicionar **notas** para cada conversa que tiver
- Acompanhe as conversas mais urgentes no seu **dashboard** e veja rapidamente quem precisa de retorno!

Depois de adicionar seu primeiro history, o dashboard vai mostrar as conversas (histories) mais urgentes primeiro. **Você pode mudar** o tempo dos **alertas de dashboard** no seu perfil, bem como sua **senha**.

## Motivação

Uma das coisas com qual trabalhei envolveu acompanhamento de clientes e parceiros de negócio e providenciar assistência e suporte. Eu pensei que seria útil criar uma ferramenta própria e com features exclusivas como minha primeira aplicação web completa!

Esse é meu projeto final para o curso [Harvard CS50's Introduction to Computer Science](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x) na edX, resultando em um certificado verificado, expandindo minha perspectiva sobre programaçaõ e abrindo meus olhos sobre como computadores e sistemas funcionam.

Eu sou grato pela equipe de Harvard e da edX fazerem este curso ser disponível para todos!

## Rodando o projeto localmente (Linux ou WSL necessário)

1. Clone ou baixe o projeto
2. (Opcional) Crie e ative o ambiente virtual

        python -m venv venv
        source venv/bin/activate

3. Instale as dependências do projeto

        pip install -r requirements.txt

4. Configure uma variável ambiente para dizer ao Flask qual é o arquivo da aplicação e rode o app

        export FLASK_APP=application
        flask run

5. Acesse `localhost:5500` (ou qualquer outro link que o terminal te der) no seu navegador

[Veja como usar](#como-usar)

## Bibliotecas e tecnologias usadas

- [CS50 IDE](https://cs50.harvard.edu/x/) como ambiente de desenvolvimento (substituído para o VS Code)
- [Heroku](https://www.heroku.com/) como plataforma cloud para hospedagem, e deploy rápido e fácil
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) para o backend
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) para comunicação com banco de dados
- [Jinja](https://palletsprojects.com/p/jinja/) como engine de template
- [SQLite](https://www.sqlite.org/) como o banco de dados
- [Bootstrap](https://getbootstrap.com/) para UI e responsividade
- [Day.js](https://day.js.org/) para tempo e data no client-side
- [Cleave.js](https://nosir.github.io/cleave.js/) para formatação automática de formulários

## Links úteis

[Galeria de projetos finais do CS50](https://cs50.harvard.edu/x/2022/gallery) **(digite FollowPhone para achar meu vídeo de apresentação que está em inglês)**  
[FollowPhone Website](https://followphone.herokuapp.com)  
[LinkedIn](https://www.linkedin.com/in/laurence-zanotti/)  
[English version of this README](https://github.com/LaurenceZanotti/cs50x2020-followphone)
