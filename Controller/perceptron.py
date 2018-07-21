'''
        --Classe para aplicar o algoritmo parceptron--
Desenvolvido por: Ronald Lopes
Data: 15/07/2018
Versão: 1.0

Status:
    >

'''
from Controller.dbClass import SinapseDB, TreinamentoDB


class Perceptron(object):
    def __init__(self):
        self.sinapses = []
        self.yDesejado= []
        # self.carregarSinapses()
        # self.geraYdesejado()
        self.epocas=0
        self.erroMinimo=0.01
        self.gama = 0.5
        self.vetorE=[] #OBS a cada epoca deve zerar esse cara!!!!!!!!
    def start(self):
        #carrega conj  para treinamento
        #Treina para cada conj
        #verifica se continua mais uma epoca ou nao (zerar o vetorE)
        # Xn =[{'valorReal': 8,'conteudo': [1,1,-1,1,1]}]
        vetorAmostras = self.carregarVetor()
        # print('Antes - Sinapses: ' + str(self.sinapses[0]))
        erroMedio=1000
        interacao= 0
        erroAtual = 0
        while(erroMedio>self.erroMinimo):
            # print('Nova geração')
            for amostras in vetorAmostras:
                self.treinar(amostras['ValorReal'], amostras['Dados'])
                # print('Treinando: '+ str(amostras['ValorReal'])+' | '+ str(amostras['Dados']))
            erroMedio = self.calculaErroMedio()

            self.vetorE=[]
            interacao = interacao +1
            print('Gama: %s , erro: %s' % (str(self.gama), str(erroMedio)))
            if(interacao==100):

                break


        print('Depois- Sinapses: '+ str(self.sinapses[0]))

    def treinaNovo(self,vetorAmostras,valorReal):
        erroMedio = 1000
        interacao = 0
        controleGama = 0
        print('Antes- Sinapses: ' + str(self.sinapses[int(valorReal-1)]))
        while (erroMedio > self.erroMinimo):
            # print('Nova geração')

            self.treinar(valorReal, vetorAmostras)
                # print('Treinando: '+ str(amostras['ValorReal']))
            erroMedio = self.calculaErroMedio()

            self.vetorE = []
            interacao = interacao + 1
            controleGama = controleGama + 1
            if (interacao == 100):
                break

        print('Erro Medio: '+ str(erroMedio))
        print('Depois- Sinapses: ' + str(self.sinapses[int(valorReal-1)]))

    def calculaErroMedio(self):
        valor = 0
        for i in self.vetorE:
            valor = valor + int(i)
        valor= valor/len(self.vetorE)
        return valor
    def treinar(self,valorReal,vetorDeTreino=[]):
        self.carregarSinapses()
        yVector=[]
        # print('Treinando valor'+str(valorReal))

        for sinapse in self.sinapses:
            yVector.append(self.geraYn(vetorDeTreino,sinapse))
        print('Y atual:'+str(yVector))
        erroCalculado,vetorErro =self.calcularErro(valorReal,yVector)
        self.vetorE.append(erroCalculado)
        self.atualizarSinapses(vetorDeTreino,vetorErro)

        self.epocas= self.epocas+1
    def geraYn(self,vector,sinapse):
        yAtual = self.geraVn(vector,sinapse)
        if(yAtual>0):
            return 1
        else:
            return -1

    def geraVn(self,vetor,sinapse):
        soma = 0
        for i in range(len(vetor)):
            soma = soma + (int(vetor[i]) * int(sinapse[i]))
        # print('SOMA '+str(soma))
        return soma

    def calcularErro(self,valorReal,vetorYatual):

        if(len(vetorYatual)==len(self.yDesejado[valorReal])): #significa q o Y desejado foi montado corretamente
            vetorErroAtual= self.geraVetorErro(valorReal,vetorYatual)
            resultado = 0
            for elemento in vetorErroAtual:
                resultado = resultado+(elemento *elemento)
            resultado = resultado/len(vetorErroAtual)
            return resultado, vetorErroAtual #sim retorno o vetor erro tbm :)
        else:
            return 1000 # valor absurdo para justamente nunca dar

    def geraVetorErro(self,valorReal=1, vetorYatual=[]):
        vetorRetorno=[]
        for i in range(len(vetorYatual)):
            temp= self.yDesejado[(valorReal-1)][i]- vetorYatual[i]
            vetorRetorno.append(temp)
        return vetorRetorno

    def atualizarSinapses(self,vetorDeTreino,vetorErro):
        bd = SinapseDB('../bd/rna')
        # print('vetor Erro: '+str(vetorErro))
        # print('Vetor de Treino:'+str(vetorDeTreino))
        # print('Sinapse inicial: '+str(self.sinapses[0]))
        for posicao in range(len(self.sinapses)):
            multiplicador= self.gama * vetorErro[posicao]
            deltaW =[]
            # print('Sinapse inicial: ' + str(self.sinapses[posicao]))
            for elemento in vetorDeTreino:
                # print(elemento)
                temp=elemento*multiplicador
                deltaW.append(int(temp))
            #deltaW pronto
            # print(len(deltaW))
            for i in range(len(self.sinapses[posicao])):
                # print("Posicao: %d, i: %d"%(posicao,i))
                self.sinapses[posicao][i]= self.sinapses[posicao][i]+deltaW[i]
            dados=[str(self.sinapses[posicao]),(posicao+1)]
            bd.atualizaSinapse(dados)
        # print('Sinapse atual: ' + str(self.sinapses[0]))
        # print('Sinapses atualizada')




    def carregarVetor(self):
        bd = TreinamentoDB('../bd/rna')
        vetorAmostras=[]
        dadosBD = bd.carregarAmostras()
        for amostra in dadosBD:
            temp = {'ValorReal':amostra[1],'Dados':self.geraSinapseFromDB(amostra[2])}
            vetorAmostras.append(temp)
        return vetorAmostras
    ###########
    def carregarSinapses(self,numeroSinapses=10, resolucao=17):
        bd = SinapseDB('../bd/rna')
        self.sinapses=[]
        for i in range(numeroSinapses):
            temp = bd.carregarSinapse((i))
            temp = self.geraSinapseFromDB(temp[1])
            self.sinapses.append((temp))

    def geraSinapseFromDB(self, sinapse=None):
        temp = sinapse.replace('[','').replace(']','').replace(' ','').split(',')
        for i in range(len(temp)):
            temp[i]=int(temp[i])
        return temp

    def gerarSinapses(self, numeroSinapses=10, resolucao=17):
        bd = SinapseDB('../bd/rna')
        for i in range(numeroSinapses):
            temp = []
            for j in range(resolucao):
                temp.append(self.aleatorio())
            # self.sinapses.append(temp)
            dados=[((i),str(temp))]
            # print(i)
            bd.registraSinapse(dados)

    def aleatorio(self):
        import random
        aleatorio= random.randint(-1, 1)
        if(aleatorio==0):
            aleatorio = self.aleatorio()
        return aleatorio


    def geraYdesejado(self, numeroDeSinapses=10):

        for i in range(numeroDeSinapses):
            vetorNulo = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
            vetorNulo[i]=1
            self.yDesejado.append(vetorNulo)

    def reconhecimento(self, vetorNovo):
        self.carregarSinapses()
        yVector = []
        # print('Treinando valor'+str(valorReal))

        for sinapse in self.sinapses:
            yVector.append(self.geraYn(vetorNovo, sinapse))
        # print('Y atual:'+str(yVector))
        for i in range(len(self.sinapses)):
            erroCalculado, vetorErro = self.calcularErro((i), yVector)
            if(erroCalculado<0.01):
                return str(i)
                # print('Numero: '+str(i+1))
        return None

perc = Perceptron()
# for i in perc.sinapses:
#     print(len(i))
# perc.start()
# perc.gerarSinapses()
perc.sinapses=[[1,1,1,1,1,1,1],[-1,-1,-1,1,1,1,1],[1,1,1,-1,-1,-1,-1]]
perc.yDesejado=[[1,-1,-1],[-1,1,-1],[-1,-1,1]]
x1=[1,1,1,1,-1,-1,-1]
x2=[1,-1,1,-1,1,1,-1]
x3=[1,-1,1,1,-1,-1,1]
perc.start()
# perc.gerarSinapses()
# perc.treinar(1,x1)
# perc.treinar(2,x2)
# perc.treinar(3,x3)
# print(perc.reconhecimento(a))