from django.shortcuts import render
from .models import Pesquisa, Envio
from django.template import RequestContext
import os.path
from django.http import HttpResponse

# Create your views here.


def home(request):
    variaveis = {}
    variaveis["linhas"] = carregar_linhas() #chama a função que vai carregar as linhas pra mostrar no template.
    variaveis["nome_tabela"] = Pesquisa._meta.verbose_name

    #pega o último id da tabela de envios que, pela lógica, é a quantidade de envios feitos.
    try:
        variaveis["total"] = Envio.objects.latest('id_envio').id_envio
    except Envio.DoesNotExist: #caso não haja o quantidade envios é igual a 0.
        variaveis["total"] = 0

    # checa qual a url do request pra saber pra qual documento html será aberto.
    if request.path == '/resultado/':
        html = 'perguntas/resultados.html'
    else:
        html = 'perguntas/home.html'

    return render(request, html, variaveis, RequestContext(request))


def envio(request):

    quantidade_perguntas = Pesquisa.objects.count()
    respondido = True
    perguntas = []
    linhas = Pesquisa.objects.all()

    #cria uma lista com todas perguntas da tabela Perguntas.
    for linha in linhas:
        perguntas.append(linha.pergunta)

    #a variável último vai definir o id do envio em questão
    try:
        ultimo = Envio.objects.latest('id_envio')
    except Envio.DoesNotExist:
        ultimo = 0

    #checar se no request.POST tem todos os names do formulário, como forma de checar se todas perguntas...
    #...foram respondidas.
    for i in range(1, quantidade_perguntas+1, 1):
        if 'op'+str(i) not in request.POST:
            respondido = False

    #caso todas tenham sido respondidas...
    if respondido:
        for i in range(1, quantidade_perguntas+1, 1):
            e = Envio()
            if ultimo == 0:
                e.id_envio = 1
            else:
                e.id_envio = ultimo.id_envio + 1

            e.pergunta = perguntas[i-1] #define a pergunta a ser inserida pela lista de perguntas criada na linha 38.
            e.resposta = request.POST["op"+str(i)] #define a resposta a ser inserida pela alternativa assinalada.
            e.save()

        variaveis = {}
        variaveis["linhas"] = carregar_linhas()
        variaveis["nome_tabela"] = Pesquisa._meta.verbose_name
        variaveis["total"] = Envio.objects.latest('id_envio').id_envio
        variaveis["mensagem"] = "Resposta enviada com sucesso"
        return render(request,'perguntas/home.html',variaveis)
    else: # caso o usuário não tenha respondido todas as perguntas o template é recarregado com a mensagem da linha 80.
        variaveis = {}
        variaveis["linhas"] = carregar_linhas()
        variaveis["nome_tabela"] = Pesquisa._meta.verbose_name
        try:
            variaveis["total"] = Envio.objects.latest('id_envio').id_envio
        except Envio.DoesNotExist:
            variaveis["total"] = 0
        variaveis["mensagem"] = "Responda todas as perguntas!"
        return render(request, 'perguntas/home.html', variaveis)



def carregar_linhas():
    # função que retorna um dicionário contendo listas com as perguntas, alternativas e imagens da tabela Pesquisa...
    # ...para serem exibidas no template.

    dados = {}
    linhas = {}
    perguntas = Pesquisa.objects.all()
    cont = 0

    for linha in perguntas:
        dados.clear()
        cont = cont + 1

        # define a imagem como uma imagem padrão caso o endereço que o adm cadastrou seja inexistente ou caso tenha...
        # optado por não inserir.
        if linha.imagem and os.path.exists('perguntas/static/imagens/' + linha.imagem):
            dados["imagem"] = "imagens/" + linha.imagem
        else:
            dados["imagem"] = "imagens/padrao.png"

        dados["pergunta"] = linha.pergunta
        dados["resposta1"] = [linha.resposta1, 0] # insere uma minilista com a resposta em si e a % que ainda será calculada
        dados["resposta2"] = [linha.resposta2, 0]
        if linha.resposta3: # só confere a existência das alternativas 3 e 4 porque as 2 primeiras são obrigatórias.
            dados["resposta3"] = [linha.resposta3, 0]
        if linha.resposta4:
            dados["resposta4"] = [linha.resposta4, 0]
        linhas[str(cont)] = dados.copy() # insere o dicionário dados no dicionário linhas e volta pro loop.

    try:  # caso já existem envios
        envios = Envio.objects.all()
        cont_linha = [0, 0, 0, 0]
        matriz_qtd = []

        i = 0
        total = []  # lista com o total de vezes que cada pergunta foi respondida, já que uma pergunta pode ser...
        # ...cadastrada pelo adm depois de já haver envios, podendo gerar diferenças de número de resposta de cada...
        # ...pergunta

        # cria uma matriz com a quatidade de vezes que cada alternativa de cada pergunta foi assinalada...
        for linha in perguntas:
            for envio in envios:
                if envio.pergunta == linha.pergunta:
                    i = i + 1
                    if envio.resposta == linha.resposta1:
                        cont_linha[0] = cont_linha[0] + 1
                    elif envio.resposta == linha.resposta2:
                        cont_linha[1] = cont_linha[1] + 1
                    elif envio.resposta == linha.resposta3:
                        cont_linha[2] = cont_linha[2] + 1
                    elif envio.resposta == linha.resposta4:
                        cont_linha[3] = cont_linha[3] + 1
            total.append(i) # ...alimenta a lista com a quantidade de vezes que cada pergunta foi respondida.
            i = 0
            matriz_qtd.append(cont_linha[:])
            cont_linha = [0, 0, 0, 0]


        x = 0
        # com base na matriz_qtd calcula a porcentagem de cada alternativa em relação a quantas vezes aquela pergunta...
        # foi respondida.

        for linha in linhas.values():
            if total[x] != 0:
                # insere no indice 1 do dict linha (ver linha 106)
                linha['resposta1'][1] = round(((matriz_qtd[x][0] / total[x]) * 100), 2)
                linha['resposta2'][1] = round(((matriz_qtd[x][1] / total[x]) * 100), 2)
                if 'resposta3' in linha:
                    linha['resposta3'][1] = round(((matriz_qtd[x][2] / total[x]) * 100), 2)
                if 'resposta4' in linha:
                    linha['resposta4'][1] = round(((matriz_qtd[x][3] / total[x]) * 100), 2)
            x = x + 1
    except Envio.DoesNotExist:  # caso não hajam envios a exception é ignorada e os indices 1 do dict linha permanecem 0.
        pass

    return linhas

