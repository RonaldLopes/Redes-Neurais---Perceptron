'''
        --Classe para processar a imagem e gerar o vetor de entrada--
Desenvolvido por: Ronald Lopes
Data: 15/07/2018
Versão: 1.0

Status:
    >

'''
import cv2


class ModuleViCompGenerator(object):
    def __init__(self,resolution=4,loadDirectory='img/',saveDirectory = 'preImg/'):
        self.resolution=resolution
        self.loadDirectory=loadDirectory
        self.saveDirectory = saveDirectory
        self.image = None
        self.vector=[]

    def readAndCreate(self,fileName="screenshot0002",width=240,height=250):
        self.vector=[]# zerar o vetor para nova conta
        saltoX = width/self.resolution
        saltoY = height/self.resolution
        self.loadDirectory= (self.loadDirectory + fileName + '.jpg') #atualiza o diretorio
        self.image = cv2.imread(self.loadDirectory) #abre a imagem
        corteInicial= self.cutImg(0,width,0,height) # ajusta a imagem para pegar apenas o essencial
        cv2.imwrite(self.loadDirectory, corteInicial) # salva a imagem ja com o corte de ajuste
        self.image = cv2.imread(self.loadDirectory) #reabre a imagem ja com o corte
        atualY=0 # variavel de controle
        atualX = 0# variavel de controle

        for i in range(self.resolution):

            for j in range(self.resolution):
                saveName= self.saveDirectory+fileName+str(i+1)+str(j+1)+'.jpg'
                imagemCortada = self.cutImg(atualX,(atualX+saltoX),atualY,(atualY+saltoY))
                # print('Coord: %d %d' %(atualX,atualY))
                # print('Coord Final: %d %d' % ((atualX+saltoX), (atualY+saltoY)))
                cv2.imwrite(saveName, imagemCortada) #Nao precisa salvar, mas é legal deixar assim
                atualX= (atualX+saltoX)
                ############### Aqui ja analisa e preenche o vetor direto##########
                self.montaVetor(img=imagemCortada,offset=80)
            atualX=0
            atualY= atualY+saltoY

    def montaVetor(self,img,offset=100):
        pixels = self.verificaQuantPixelsvalidos(img=img)
        # print('Pixel valido: ' + str(pixels))
        if(int(pixels)>offset):
            self.vector.append(1)

        else:
            self.vector.append(-1)

    def verificaQuantPixelsvalidos(self,img, nivelCorMin=190):
        conta = 0
        # vou percorrer cada pixel da imagem e verificar
        for i in img: #percorrendo linhas
            for j in i: #Percorrenco colunas da linha atual
                contador = 0
                for k in j: #vendo elementos e verificando a cor
                    if (k > nivelCorMin):
                        contador = contador + 1
                if (contador == 3): #se cor for cinza ou branco é valido entao contabiliza
                    conta = conta + 1
        return conta #retorna a quantidade de pixels validos


    def cutImg(self, xIni,xFim,yIni,yFim):
        corte = self.image[int(yIni):int(yFim),int(xIni):int(xFim)]
        return corte
    def show(self): #temporario
        cv2.imshow("original", self.image)
        cv2.waitKey(0)
    def showCut(self): #temporario
        cropped = self.image[0:60,60:120]
        cv2.imshow("cropped", cropped)
        cv2.waitKey(0)

# test = ModuleViCompGenerator()
# test.readAndCreate(fileName='numero0001')
# # test.showCut()
# # test.show()
# print(test.vector)