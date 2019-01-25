# projeto-django
Aplicação web com um questionário dinâmico, feito pra exercer e aprofundar os conhecimentos do framework Django.

# Funcionamento
Questionário simples, com perguntas vindo do banco de dados. O template do questionário é aberto apenas pelo endereço do servidor. Há também um template que mostra a porcentagem da votos de cada alternativa em relação a quantidade respostas que aquela pergunta recebeu, que é aberto pela url /resultado.
O envio só pode ser feito caso todas as perguntas estejam com uma alternativa marcada, porém é possível, como será explicado, cadastrar mais perguntas depois que envios já tenham sido feitos, por isso a porcentagem mostrada é em relação a quantidade de envios de cada pergunta.

# Django Admin
O administrador pode cadastrar até dez perguntas, cada uma com o mínimo de duas e o máximo de quatro alternativas, além de modificá-las e deletá-las. Em relação são aos envios, o administrador por alterá-los e deletá-los mas a inclusão de novos envios só é feita por código.
Dados para logar: 
usuário: admin
senha: admin

# Imagem 
O administrador deve incluir a nome de imagem presente na pasta imagem presente na pasta static da aplicação + a extensão no campo Imagem na hora de cadastrar uma pergunta. Caso opte por não incluir imagem ou o nome seja inválido uma imagem padrão será exibida no template.



