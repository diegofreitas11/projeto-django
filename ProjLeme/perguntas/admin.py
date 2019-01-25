from django.contrib import admin
from .models import Pesquisa, Envio


class EnvioAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

class PesquisaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if Pesquisa.objects.count() >= 10: #não permite que adm cadastre mais de 10 perguntas.
            return False
        else:
            return True

    #override no save_model pra caso o usuário editar a pergunta, ele também mude na tabela de envios
    def save_model(self, request, obj, form, change):
        pesquisa = Pesquisa.objects.all()

        anterior = ""
        anterior_alternativa = ["","","",""]

        for linha in pesquisa:
            if linha.id == obj.id:
                anterior = linha.pergunta
                anterior_alternativa = [linha.resposta1, linha.resposta2, linha.resposta3 or None, linha.resposta4 or None]


        envios = Envio.objects.all()
        for envio in envios:
            e = Envio.objects.get(id_envio=envio.id_envio, pergunta=envio.pergunta)
            if anterior == envio.pergunta:
                e.pergunta = request.POST.get('pergunta')

                for i in range(0,4,1):
                    if anterior_alternativa[i] == envio.resposta:
                        e.resposta = request.POST.get('resposta'+str(i+1))

            e.save()


        super(PesquisaAdmin, self).save_model(request, obj, form, change)


admin.site.register(Pesquisa, PesquisaAdmin)
admin.site.register(Envio, EnvioAdmin)



# Register your models here.
