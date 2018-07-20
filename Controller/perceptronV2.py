from Controller.dbClass import TreinamentoDB, SinapseDB


class PerceptronV2(object):
    def __init__(self):
        self.sinapses = []
        self.yDesejado = []
        self.epocas = 0
        self.erroMedioMinimo = 0.01
        self.gama = 0.5
        self.vetorErro = []
        self.resolucao=17
        self.numeroSinapses=10

    def configura(self):
        self.gerarSinapses()

    def gerarSinapses(self):
        bd = SinapseDB('bd/rna')
        for i in range(self.numeroSinapses):
            temp = []
            for j in range(self.resolucao):
                temp.append(self.aleatorio())
            dados = [((i), str(temp))]
            bd.registraSinapse(dados)

    def aleatorio(self):
        import random
        aleatorio= random.randint(-1, 1)
        if(aleatorio==0):
            aleatorio = self.aleatorio()
        return aleatorio

    def geraYdesejado(self):

        for i in range(self.numeroSinapses):
            vetorNulo = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            vetorNulo[i]=1
            self.yDesejado.append(vetorNulo)

    def preparaEtreina(self):
        vetorEntrada= self.carregarVetor()
        self.carregarSinapses()
        self.geraYdesejado()
        self.start(vetorEntrada)
        # self.start(vetorEntrada)
    def salvaSinapsesNoBD(self):
        bd = SinapseDB('bd/rna')
        for erro in range(len(self.sinapses)):
            dados = [str(self.sinapses[erro]), (erro)]
            bd.atualizaSinapse(dados)

    def carregarSinapses(self):
        bd = SinapseDB('bd/rna')
        self.sinapses=[]
        for i in range(self.numeroSinapses):
            temp = bd.carregarSinapse((i))
            temp = self.geraDadoFromDB(temp[1])
            self.sinapses.append((temp))

    def carregarVetor(self):
        bd = TreinamentoDB('bd/rna')
        vetorAmostras = []
        dadosBD = bd.carregarAmostras()
        for amostra in dadosBD:
            temp = {'ValorReal': amostra[1], 'Dados': self.geraDadoFromDB(amostra[2])}
            vetorAmostras.append(temp)
        return vetorAmostras

    def geraDadoFromDB(self, sinapse=None):
        temp = sinapse.replace('[','').replace(']','').replace(' ','').split(',')
        for i in range(len(temp)):
            temp[i]=int(temp[i])
        return temp

    def start(self,vetorAmostras):
        while(True):
            for amostra in vetorAmostras:
                self.iniciarTreinamento(amostra['ValorReal'],amostra['Dados'])
            erroMedio = self.calculaErroMedio()
            print('Erro: '+str(erroMedio))
            if(erroMedio<self.erroMedioMinimo):
                self.salvaSinapsesNoBD()
                break

    def treinaAmostraUnica(self,vetorAmostra): #treinar apenas 1 amostra
        self.carregarSinapses()
        self.geraYdesejado()
        while(True):
            self.iniciarTreinamento(vetorAmostra['ValorReal'],vetorAmostra['Dados'])
            erroMedio = self.calculaErroMedio()
            print('Erro: '+str(erroMedio))
            if(erroMedio<self.erroMedioMinimo):
                self.salvaSinapsesNoBD()
                break

    def calculaErroMedio(self):
        erroMedio=0
        for i in self.vetorErro:
            erroMedio= erroMedio+ i
        erroMedio = erroMedio/(len(self.vetorErro))
        return erroMedio

    def iniciarTreinamento(self, valorReal, vetorDeTreinamento):

        vetorY = self.geraVetorY(self.geraVn(vetorDeTreinamento))
        valorE, vetorErroAtual = self.calculaErro(self.geraVetorErro(valorReal, vetorY))
        self.vetorErro.append(valorE)
        self.atualizaSinapses(vetorErroAtual,vetorDeTreinamento)

    def atualizaSinapses(self,vetorErroAtual, vetor):

        for erro in range(len(vetorErroAtual)):
            deltaW = self.deltaW(vetorErroAtual[erro],vetor)
            self.sinapses[erro]= self.somaVetor(self.sinapses[erro],deltaW)
            #updateDBSinapse aqui

    def analisaVetor(self,vetorDeAnalise):
        self.carregarSinapses()
        self.geraYdesejado()
        for pos in range(len(self.yDesejado)):
            vetorY = self.geraVetorY(self.geraVn(vetorDeAnalise))
            valorE, vetorErroAtual = self.calculaErro(self.geraVetorErro(pos, vetorY))
            # print('Valor do Erro obtido: '+str(valorE))
            if(valorE==0):
                return pos
        return None
    def somaVetor(self,vetor,delta):
        vetorResposta=[]
        for pos in range(len(vetor)):
            vetorResposta.append((vetor[pos]+delta[pos]))
        return  vetorResposta

    def deltaW(self,erro,vetor):
        delta=[]
        for posicao in range(len(vetor)):
            delta.append(int(vetor[posicao]*self.gama*erro))
        return delta

    def geraVetorErro(self,valorReal,vetor):
        vetorErro = []
        for posicao in range(len(vetor)):
            vetorErro.append((self.yDesejado[valorReal][posicao]-vetor[posicao]))
        return vetorErro

    def calculaErro(self,vetorErro):
        valorErro=0
        for erro in vetorErro:
            valorErro= valorErro +(erro*erro)
        valorErro = (valorErro/len(vetorErro))
        return valorErro, vetorErro

    def geraVn(self,vetor):
        vetorVn=[]
        for sinapse in self.sinapses:
            somatorio = 0
            for posicao in range(len(sinapse)):
                somatorio= somatorio+(vetor[posicao]*sinapse[posicao])
            vetorVn.append(somatorio)

        return vetorVn

    def geraVetorY(self,vetorVn):
        vetorY=[]
        for i in vetorVn:
            if(i>0):
                vetorY.append(1)
            else:
                vetorY.append(-1)
        return  vetorY

# perc = PerceptronV2()
# perc.sinapses=[[1,1,1,1,1,1,1],[-1,-1,-1,1,1,1,1],[1,1,1,-1,-1,-1,-1]]
# perc.yDesejado=[[1,-1,-1],[-1,1,-1],[-1,-1,1]]
# perc.resolucao=7
# perc.numeroSinapses=3
# entrada =[{'ValorReal':0,'Dados':[1,1,1,1,-1,-1,-1]},
# {'ValorReal':1,'Dados':[1,-1,1,-1,1,1,-1]},
# {'ValorReal':2,'Dados':[1,-1,1,1,-1,-1,1]}]
# re =perc.analisaVetor([1,1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1])
# print(re)
# perc.start(entrada)
# perc.preparaEtreina()
# perc.configura()
# amostra={'ValorReal':5,'Dados':[1,1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1]}
# perc.treinaAmostraUnica(amostra)