'''
Módulo para testes das funções de todo o repositório.
'''

from utils_gabriel import cria_imc,df_allyears,read_local_data
import pandas as pd
from cleandata import make_http_request,process_data
from downloaddata import download_csv_local
import unittest
import os

class TestMakeHttpRequest(unittest.TestCase):
    '''
    Classe de teste para a função make_https_request do módulo cleandata.
    '''
    def test_failed_request(self):
        '''
        Teste com https inexistente
        '''
        url_falha = 'https://www.exemplo.com/pagina_inexistente'
        resposta_falha = make_http_request(url_falha)
        self.assertIsNone(resposta_falha)


class TestDownloadCSVLocal(unittest.TestCase):
    '''
    Classe de teste para a função download_csv_local.
    '''
    def setUp(self):
        '''
        Define a URL de teste e o caminho local do arquivo.
        '''
        self.test_url = 'https://dadosabertos.eb.mil.br/arquivos/sermil/sermil2022.csv'
        self.local_file_path = 'test_data.csv'

    def tearDown(self):
        '''
        Exclui o arquivo CSV de teste se ele existir.
        '''
        if os.path.exists(self.local_file_path):
            os.remove(self.local_file_path)

    def test_download_csv_local(self):
        '''
        Verifica se o arquivo foi criado e se não está vazio.
        '''
        download_csv_local(self.test_url,self.local_file_path)

        
        self.assertTrue(os.path.exists(self.local_file_path), "O arquivo CSV não foi baixado localmente")

        
        self.assertTrue(os.path.getsize(self.local_file_path) > 0, "O arquivo CSV está vazio")
        

class TestCriaIMC(unittest.TestCase):
    '''
    Classe de teste para a função cria_imc do módulo utils_gabriel.

    Esta classe de teste verifica a função cria_imc para garantir que ela funcione
    corretamente e lida com diferentes cenários, como valores não numéricos, altura zero,
    peso zero, altura negativa e peso negativo.
    '''
    def test_cria_imc_correct(self):
        '''
        Teste com a função cria_imc dando certo.
        '''
        
        # Dados de teste
        dados = {'Altura(cm)': [160, 175, 150, 180],
                 'Peso(kg)': [65, 80, 55, 90]}
        df = pd.DataFrame(dados)

        
        df_resultado = cria_imc(df, 'Altura(cm)', 'Peso(kg)')

        # Valores esperados após o cálculo do IMC
        valores_esperados = [25.390625, 26.122449, 24.444444, 27.777778]

        # Verifica se os valores da coluna IMC correspondem aos valores esperados
        for i, valor_esperado in enumerate(valores_esperados):
            self.assertAlmostEqual(df_resultado.loc[i, 'IMC'], valor_esperado, places=2)

        # Verifica se a coluna 'Altura(cm)' foi removida
        self.assertNotIn('Altura(cm)', df_resultado.columns)

    def test_valores_nao_numericos_altura(self):
        '''
        Teste com a função cria_imc com valor não numérico.
        '''
        
        # Dados de teste com valores não numéricos na coluna de altura
        dados = {'Altura(cm)': ['160', 175, 150, 180],
                 'Peso(kg)': [65, 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando há valores não numéricos
        resultado = cria_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)

    def test_altura_zero(self):
        '''
        Teste com a função cria_imc com valor na coluna altura igual a zero.
        '''
        # Dados de teste com altura igual a zero
        dados = {'Altura(cm)': [0, 175, 150, 180],
                 'Peso(kg)': [65, 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando a altura é zero
        resultado = cria_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)

    def test_altura_negativa(self):
        '''
        Teste com a função cria_imc com valor na coluna altura menor que zero.
        '''        
        # Dados de teste com altura negativa
        dados = {'Altura(cm)': [-160, 175, 150, 180],
                 'Peso(kg)': [65, 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando a altura é negativa
        resultado = cria_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)

    def test_valores_nao_numericos_peso(self):
        '''
        Teste com a função cria_imc com valor na coluna peso não numérico.
        '''   
        # Dados de teste com valores não numéricos na coluna de peso
        dados = {'Altura(cm)': [160, 175, 150, 180],
                 'Peso(kg)': ['65', 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando há valores não numéricos
        resultado = cria_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)

    def test_peso_zero(self):
        '''
        Teste com a função cria_imc com valor na coluna peso igual a zero.
        '''   
        # Dados de teste com peso igual a zero
        dados = {'Altura(cm)': [160, 175, 150, 180],
                 'Peso(kg)': [0, 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando o peso é zero
        resultado = cria_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)

    def test_peso_negativo(self):
        '''
        Teste com a função cria_imc com valor na coluna peso menor que zero.
        '''           
        # Dados de teste com peso negativo
        dados = {'Altura(cm)': [160, 175, 150, 180],
                 'Peso(kg)': [-65, 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando o peso é negativo
        resultado = cria_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)


class TestProcessData(unittest.TestCase):
    """
    Classe de teste para a função process_data.

    Esta classe de teste verifica a função process_data para garantir que ela funcione
    corretamente em diferentes cenários, incluindo processamento completo, colunas inválidas
    e manipulação de valores nulos.

    """

    def test_processamento_completo(self):
        """
        Testa o processamento completo de dados.

        Verifica se as colunas esperadas estão presentes, se não há valores nulos
        e se o resultado é um DataFrame.

        """
        # Dados de teste completos
        dados_teste = '''Nome,Idade,Sexo
        João,30,M
        Maria,25,F
        Carlos,35,M
        Ana,28,F
        '''
        resultado = process_data(dados_teste)
        
        # Verifica se o resultado é um DataFrame
        self.assertIsInstance(resultado, pd.DataFrame)
        
        # Verifica se as colunas esperadas estão presentes
        colunas_esperadas = ['Nome', 'Idade', 'Sexo']
        for coluna in colunas_esperadas:
            self.assertIn(coluna, resultado.columns)

        # Verifica se não há valores nulos
        self.assertFalse(resultado.isnull().values.any())

    def test_colunas_invalidas(self):
        """
        Testa o cenário em que colunas inválidas são especificadas.

        Verifica se a função retorna None quando colunas inválidas são especificadas.

        """
        # Dados de teste com colunas inválidas
        dados_teste = '''
        Nome,Idade,Sexo
        João,30,M
        Maria,25,F
        Carlos,35,M
        Ana,28,F
        '''
        colunas_invalidas = ['Nome', 1, 'Idade']
        resultado = process_data(dados_teste, desired_columns=colunas_invalidas)
        
        # Verifica se o resultado é None
        self.assertIsNone(resultado)

    def test_dropnull_true(self):
        """
        Testa o cenário em que `dropnull` é definido como True.

        Verifica se não há valores nulos no resultado quando `dropnull` é True.

        """
        # Dados de teste com valores nulos
        dados_teste = '''
        Nome,Idade,Sexo
        João,30,M
        Maria,,F
        Carlos,35,M
        Ana,28,F
        '''
        resultado = process_data(dados_teste, dropnull=True)
        
        # Verifica se o resultado é um DataFrame
        self.assertIsInstance(resultado, pd.DataFrame)
        
        # Verifica se não há valores nulos
        self.assertFalse(resultado.isnull().values.any())


class TestDfAllYears(unittest.TestCase):
    '''
    Classe de teste da função df_allyears do módulo utils_gabrie.
    '''
    def test_concatenacao_dataframes(self):
        '''
        Teste em que funciona o concatenamento de tabelas.
        '''
        # Dados de teste: três DataFrames com as mesmas colunas
        data1 = {'Ano': [2007, 2008],
                 'Alistados': [1000, 1100]}
        data2 = {'Ano': [2009, 2010],
                 'Alistados': [1200, 1300]}
        data3 = {'Ano': [2011, 2012],
                 'Alistados': [1400, 1500]}
        
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        df3 = pd.DataFrame(data3)

        data_list = [df1, df2, df3]
        
        # Testa se a função retorna um DataFrame
        resultado = df_allyears(data_list)
        self.assertIsInstance(resultado, pd.DataFrame)
        
        # Testa se o DataFrame concatenado tem o mesmo número de linhas que a soma dos DataFrames individuais
        self.assertEqual(len(resultado), len(df1) + len(df2) + len(df3))

    def test_nomes_colunas_diferentes(self):
        '''
        Teste que confere se ao passar datasets que possuem colunas
        com nomes diferentes levanta o tratamento realizado.
        '''
        # Dados de teste: três DataFrames com nomes de colunas diferentes
        data1 = {'Ano': [2007, 2008],
                 'Alistados': [1000, 1100]}
        data2 = {'Year': [2009, 2010],
                 'Enlistment': [1200, 1300]}
        data3 = {'Year': [2011, 2012],
                 'Recruits': [1400, 1500]}
        
        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        df3 = pd.DataFrame(data3)

        data_list = [df1, df2, df3]
        
        # Testa se a função gera um erro ValueError quando os nomes das colunas são diferentes
        resultado = df_allyears(data_list)
        self.assertIsNone(resultado)

    def test_lista_com_menos_de_dois_dataframes(self):
        '''
        Teste que confere se ao passar menos de dois dataframes
        levanta o tratamento realizado.
        '''
        # Dados de teste: uma lista com apenas um DataFrame
        data = {'Ano': [2007, 2008],
                'Alistados': [1000, 1100]}
        df = pd.DataFrame(data)

        data_list = [df]
        
        # Testa se a função gera um erro ValueError quando a lista contém menos de dois DataFrames
        resultado = df_allyears(data_list)
        self.assertIsNone(resultado)


class TestReadLocalData(unittest.TestCase):
    '''
    Classe de teste para a função read_local_data.
    '''

    def test_leitura_arquivo_existente(self):
        '''
        Teste se a função lê um arquivo CSV existente corretamente.

        Cria um arquivo CSV de teste temporário, lê o arquivo e verifica se o resultado
        é um DataFrame com as mesmas dimensões que o DataFrame original. Em seguida,
        exclui o arquivo de teste temporário.

        '''
        # Cria um arquivo CSV de teste temporário
        arquivo_teste = 'arquivo_teste.csv'
        data = {'Coluna1': [1, 2, 3],
                'Coluna2': ['A', 'B', 'C']}
        df = pd.DataFrame(data)
        df.to_csv(arquivo_teste, index=False)

        # Testa se a função lê o arquivo CSV existente corretamente
        resultado = read_local_data(arquivo_teste)
        
        # Verifica se o resultado é um DataFrame
        self.assertIsInstance(resultado, pd.DataFrame)
        
        # Verifica se o DataFrame tem o mesmo número de linhas e colunas que o DataFrame original
        self.assertEqual(resultado.shape, df.shape)

        # Limpeza: Exclua o arquivo de teste temporário
        os.remove(arquivo_teste)

    def test_arquivo_inexistente(self):
        '''
        Teste se a função gera um erro NameError quando o arquivo não existe.

        Tenta ler um arquivo que não existe e verifica se a função gera um erro NameError.

        '''
        # Testa se a função gera um erro NameError quando o arquivo não existe
        arquivo_inexistente = 'arquivo_inexistente.csv'
        resultado = read_local_data(arquivo_inexistente)
        
        # Verifica se o resultado é None
        self.assertIsNone(resultado)

    def test_erro_leitura(self):
        '''
        Teste se a função gera uma exceção ao tentar ler um diretório em vez de um arquivo.

        Cria um diretório de teste temporário para simular um erro de leitura e tenta ler
        esse diretório. Em seguida, verifica se a função gera uma exceção.

        '''
        # Cria um diretório de teste temporário para simular um erro de leitura
        diretorio_teste = 'diretorio_teste'
        os.makedirs(diretorio_teste)

        # Tenta ler um diretório em vez de um arquivo
        try:
            read_local_data(diretorio_teste)
        except Exception as e:
            # Verifica se a função gera um erro (uma exceção)
            self.assertIsInstance(e, Exception)

        # Limpeza: Remova o diretório de teste temporário
        os.rmdir(diretorio_teste)

if __name__ == '__main__':
    unittest.main()