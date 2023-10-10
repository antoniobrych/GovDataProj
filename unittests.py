'''
Modulo para testes das funcoes de todo o repositorio.
'''

from utils_gabriel import df_allyears,read_local_data,filtra,mean,median
import pandas as pd
from cleandata import make_http_request,process_data
from downloaddata import download_csv_local
import unittest
import os

class TestMakeHttpRequest(unittest.TestCase):
    '''
    Classe de teste para a funcao make_https_request do modulo cleandata.
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
    Classe de teste para a funcao download_csv_local.
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
        Verifica se o arquivo foi criado e se nao esta vazio.
        '''
        download_csv_local(self.test_url,self.local_file_path)

        
        self.assertTrue(os.path.exists(self.local_file_path), "O arquivo CSV não foi baixado localmente")

        
        self.assertTrue(os.path.getsize(self.local_file_path) > 0, "O arquivo CSV está vazio")
        



class TestProcessData(unittest.TestCase):
    """
    Classe de teste para a funcaoo process_data.

    Esta classe de teste verifica a função process_data para garantir que ela funcione
    corretamente em diferentes cenarios, incluindo processamento completo, colunas invalidas
    e manipulacao de valores nulos.

    """

    def test_processamento_completo(self):
        """
        Testa o processamento completo de dados.

        Verifica se as colunas esperadas estão presentes, se nao ha valores nulos
        e se o resultado sera um DataFrame.

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
        Testa o cenario em que colunas invalidas sao especificadas.

        Verifica se a funcao retorna None quando colunas invalidas sao especificadas.

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
        Testa o cenario em que `dropnull` sera definido como True.

        Verifica se nao ha valores nulos no resultado quando `dropnull` for True.

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
    Classe de teste da funcao df_allyears do modulo utils_gabrie.
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
    Classe de teste para a funcao read_local_data.
    '''

    def test_leitura_arquivo_existente(self):
        '''
        Teste se a funcao le um arquivo CSV existente corretamente.

        Cria um arquivo CSV de teste temporário, le o arquivo e verifica se o resultado
        sera um DataFrame com as mesmas dimensoes que o DataFrame original. Em seguida,
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
        Teste se a funcao gera uma excecao ao tentar ler um diretorio em vez de um arquivo.

        Cria um diretorio de teste temporario para simular um erro de leitura e tenta ler
        esse diretorio. Em seguida, verifica se a funcao gera uma excecao.

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

    def test_selected_columns(self):
        '''
        Testa a funcao read_local_data para garantir que ela le corretamente um arquivo CSV
        com colunas selecionadas e retorna um DataFrame contendo apenas as colunas especificadas.
    
        Para este teste, um arquivo CSV de exemplo sera criado com as colunas 'A', 'B' e 'C', 
        e a funcao read_local_data sera chamada para ler apenas as colunas 'A' e 'C'. 
        Em seguida, verifica se o DataFrame resultante possui exatamente as colunas
        especificadas.
        
        '''
        # Cria um arquivo CSV de exemplo
        sample_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
        sample_data.to_csv('sample_data.csv', index=False)

        # Chama a função para ler o arquivo CSV com colunas selecionadas
        selected_cols = ['A', 'C']
        df = read_local_data('sample_data.csv', cols=selected_cols)

        # Verifica se o DataFrame possui apenas as colunas selecionadas
        self.assertListEqual(list(df.columns), selected_cols)

    def test_dropnull_true(self):
        # Cria um DataFrame de exemplo para o teste
        data = {'A': [1, 2, 3, None],
                'B': ['foo', 'bar', 'foo', 'baz']}
        self.df = pd.DataFrame(data)

        
        # Cria um arquivo CSV temporario para o teste
        temp_csv_file = 'temp_test_file.csv'
        self.df.to_csv(temp_csv_file, index=False)

        # Chame a função com dropnull = True
        df_com_nulls_removidos = read_local_data(temp_csv_file, dropnull=True)

        # Verifica se as linhas nulas foram removidas
        self.assertFalse(df_com_nulls_removidos.isnull().values.any())

        # Remova o arquivo CSV temporário após o teste
        os.remove(temp_csv_file)


class TesteFuncaoFiltra(unittest.TestCase):
    '''
    Classe de teste para a funcao que filtra tabelas com
    uma condicao de igualdade.
    '''
    def setUp(self):
        '''
        Cria um DataFrame de exemplo para os testes.
        '''
        data = {'A': [1, 2, 3, 4],
                'B': ['foo', 'bar', 'foo', 'baz']}
        self.df = pd.DataFrame(data)

    def test_filtra_sucesso(self):
        '''
        Teste dando certo. 
        '''
        dados_filtrados = filtra(self.df, 'B', 'foo')
        self.assertTrue(dados_filtrados.equals(pd.DataFrame({'A': [1, 3], 'B': ['foo', 'foo']})))

    def test_filtra_coluna_nao_encontrada(self):
        '''
        Teste com coluna que nao existe no dataset.
        '''
        with self.assertRaises(KeyError):
            filtra(self.df, 'C', 'valor_nao_existente_na_coluna')


class TestMeanFunction(unittest.TestCase):
    '''
    Classe de teste para a funcao mean do modulo utils_gabriel.
    '''
    def setUp(self):
        data = {'Valor': [1, 2, 3, 4, 5],
                'Texto': ['A', 'B', 'C', 'D', 'E']}
        self.df = pd.DataFrame(data)

    def test_mean_calculation(self):
        '''
        Testa o cálculo da média para uma coluna numérica.
        Verifica se o resultado é uma instância de int ou float e se está correto.
        '''        
        media = mean(self.df, 'Valor')
        self.assertIsInstance(media, (int, float))
        self.assertAlmostEqual(media, 3.0)

    def test_mean_non_numeric_column(self):
        '''
        Testa a função quando aplicada a uma coluna não numérica.
        Deve levantar uma exceção ValueError.
        '''        
        with self.assertRaises(ValueError):
            mean(self.df, 'Texto')


class TestMedianFunction(unittest.TestCase):
    '''
    Classe de teste para a funcao mediana do modulo utils_gabriel
    '''
    def setUp(self):
        data = {'Valor': [1, 2, 3, 4, 5],
                'Texto': ['A', 'B', 'C', 'D', 'E']}
        self.df = pd.DataFrame(data)

    def test_median_calculation(self):
        '''
        Testa o cálculo da mediana para uma coluna numérica.
        Verifica se o resultado é uma instância de int ou float e se está correto.
        '''
        mediana = median(self.df, 'Valor')
        self.assertIsInstance(mediana, (int, float))
        self.assertAlmostEqual(mediana, 3.0)

    def test_median_non_numeric_column(self):
        '''
        Testa a função quando aplicada a uma coluna não numérica.
        Deve levantar uma exceção ValueError.
        '''
        with self.assertRaises(ValueError):
            median(self.df, 'Texto')


if __name__ == '__main__':
    unittest.main()