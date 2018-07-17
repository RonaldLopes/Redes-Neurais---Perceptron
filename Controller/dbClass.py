'''
        --Classe para conectar ao banco de dados--
Desenvolvido por: Ronald Lopes
Data: 15/07/2018
Versão: 1.0

Status:
    >

'''
import sqlite3

class Conect(object):
    '''Desenvolvido por: Ronald Lopes'''
    '''Classe para conectar ao banco de dados'''
    def __init__(self, dbNome):

        try:

            self.conectar = sqlite3.connect(dbNome)
            # print(self.conectar)
            self.cursor = self.conectar.cursor()
            # print('Banco: ',dbNome)
        except sqlite3.Error as e:
            print(e)
            print("Erro no banco de dados")

    def desconectar(self):
        if self.conectar:
            self.conectar.close()
            print("Conexão encerrada")

    def gravar(self):
        if  self.conectar:
            self.conectar.commit()
        else:
            print('Error')

class SinapseDB(object):
    def __init__(self,nomeBD):
        self.bancoDeDados= Conect(nomeBD)
        self.tabela = "sinapses"

    def registraSinapse(self,dados=[()]):
        self.bancoDeDados.cursor.executemany("""
        INSERT INTO sinapses (ID,Conteudo)
        VALUES (?,?)
        """,dados)
        self.bancoDeDados.gravar()
        print("Escrita log de sinapse no DB efetuada")
    def atualizaSinapse(self,dados):
        self.bancoDeDados.cursor.execute("""
        UPDATE sinapses 
        SET Conteudo = ?
        WHERE id = ?
        """, (dados))
        self.bancoDeDados.gravar()
    def carregarSinapse(self,id):
        r = self.bancoDeDados.cursor.execute(
            'SELECT * FROM sinapses WHERE ID = ? ',(str(id),) )
        return r.fetchone()

class TreinamentoDB(object):
    def __init__(self,nomeBD):
        self.bancoDeDados= Conect(nomeBD)
        self.tabela = "treinamento"

    def registraTreinamento(self,dados=[()]):
        self.bancoDeDados.cursor.executemany("""
        INSERT INTO treinamento (ID,Significado,Conteudo)
        VALUES (?,?,?)
        """,dados)
        self.bancoDeDados.gravar()
        print("Escrita log de treinamento no DB efetuada")

    def carregarAmostras(self):
        r = self.bancoDeDados.cursor.execute(
            'SELECT * FROM treinamento WHERE ID ', )
        return r.fetchall()