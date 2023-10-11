'''
Modulo para testes das funcoes criadas pelo Gabriel.
'''

from utilsgabriel import create_imc, read_local_data, percentage_value_counts, df_allyears
import pandas as pd
from cleandata import make_http_request, process_data, clean_dataframe
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
        

class TestCreateIMC(unittest.TestCase):
    '''
    Classe de teste para a funcao create_imc do modulo utilsgabriel.

    Esta classe de teste verifica a função cria_imc para garantir que ela funcione
    corretamente e lida com diferentes cenarios, como valores nao numericos, altura zero,
    peso zero, altura negativa e peso negativo.
    '''
    def test_create_imc_correct(self):
        '''
        Teste com a funcao create_imc dando certo.
        '''
        
        # Dados de teste
        dados = {'Altura(cm)': [160, 175, 150, 180],
                 'Peso(kg)': [65, 80, 55, 90]}
        df = pd.DataFrame(dados)

        
        df_resultado = create_imc(df, 'Altura(cm)', 'Peso(kg)')

        # Valores esperados após o cálculo do IMC
        valores_esperados = [25.390625, 26.122449, 24.444444, 27.777778]

        # Verifica se os valores da coluna IMC correspondem aos valores esperados
        for i, valor_esperado in enumerate(valores_esperados):
            self.assertAlmostEqual(df_resultado.loc[i, 'IMC'], valor_esperado, places=2)

        # Verifica se a coluna 'Altura(cm)' foi removida
        self.assertNotIn('Altura(cm)', df_resultado.columns)

    def test_non_numeric_values_height(self):
        '''
        Teste com a funcao create_imc com valor nao numerico.
        '''
        
        # Dados de teste com valores não numéricos na coluna de altura
        dados = {'Altura(cm)': ['160', 175, 150, 180],
                 'Peso(kg)': [65, 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando há valores não numéricos
        resultado = create_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)

    def test_height_zero(self):
        '''
        Teste com a funcao create_imc com valor na coluna altura igual a zero.
        '''
        # Dados de teste com altura igual a zero
        dados = {'Altura(cm)': [0, 175, 150, 180],
                 'Peso(kg)': [65, 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando a altura é zero
        resultado = create_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)

    def test_negative_height(self):
        '''
        Teste com a funcao create_imc com valor na coluna altura menor que zero.
        '''        
        # Dados de teste com altura negativa
        dados = {'Altura(cm)': [-160, 175, 150, 180],
                 'Peso(kg)': [65, 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando a altura é negativa
        resultado = create_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)

    def test_non_numeric_values_weight(self):
        '''
        Teste com a funcao create_imc com valor na coluna peso nao numerico.
        '''   
        # Dados de teste com valores não numéricos na coluna de peso
        dados = {'Altura(cm)': [160, 175, 150, 180],
                 'Peso(kg)': ['65', 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando há valores não numéricos
        resultado = create_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)

    def test_weight_zero(self):
        '''
        Teste com a funcao create_imc com valor na coluna peso igual a zero.
        '''   
        # Dados de teste com peso igual a zero
        dados = {'Altura(cm)': [160, 175, 150, 180],
                 'Peso(kg)': [0, 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando o peso é zero
        resultado = create_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)

    def test_negative_weight(self):
        '''
        Teste com a função create_imc com valor na coluna peso menor que zero.
        '''           
        # Dados de teste com peso negativo
        dados = {'Altura(cm)': [160, 175, 150, 180],
                 'Peso(kg)': [-65, 80, 55, 90]}
        df = pd.DataFrame(dados)

        # Verifica se a função retorna None quando o peso é negativo
        resultado = create_imc(df, 'Altura(cm)', 'Peso(kg)')
        self.assertIsNone(resultado)


class TestProcessData(unittest.TestCase):
    """
    Classe de teste para a funcaoo process_data.

    Esta classe de teste verifica a função process_data para garantir que ela funcione
    corretamente em diferentes cenarios, incluindo processamento completo, colunas invalidas
    e manipulacao de valores nulos.

    """

    def test_process_correct(self):
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

    def test_invalid_columns(self):
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
    Classe de teste da funcao df_allyears do modulo utilsgabriel.
    '''
    def test_concat_dataframes_correct(self):
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

    def test_different_column_names(self):
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

    def test_less_than_two_dfs(self):
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
      

class TestPercentageValueCounts(unittest.TestCase):
    '''
    Classe de teste para a funcao percentage_value_counts.
    '''
    def test_percentage_value_counts(self):
        '''
        Teste com o return esperado.
        '''        
        dados = pd.Series([1, 2, 2, 2, 3, 4, 4, 4, 5, 5])
        result = percentage_value_counts(dados)

        expected_result = pd.DataFrame({'PORCENTAGEM': [0.1, 0.3, 0.3, 0.1, 0.2]}, index=[1, 2, 4, 3, 5])

        # Ordena os índices de result e expected_result antes da comparação
        result = result.sort_index()
        expected_result = expected_result.sort_index()

        self.assertTrue(result.equals(expected_result))
        
    def test2_percentage_value_counts(self):
        '''
        Teste com números diferentes.
        '''        
        dados = pd.Series([2, 2, 3, 3, 3, 4, 4, 4, 4, 5])
        result = percentage_value_counts(dados)

        expected_result = pd.DataFrame({'PORCENTAGEM': [0.2, 0.3, 0.4, 0.1]}, index=[2, 3, 4, 5])

        # Ordena os índices de result e expected_result antes da comparação
        result = result.sort_index()
        expected_result = expected_result.sort_index()

        self.assertTrue(result.equals(expected_result))


class TestCleanDataFrame(unittest.TestCase):
    '''
    Classe de teste para a funcao clean_dataframe do modulo utilsgabriel.
    '''
    def test_clean_dataframe_columns_drop(self):
        '''
        Testa se as colunas especificadas são removidas corretamente
        '''
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
        cleaned_df = clean_dataframe(df, columns_to_drop=['A', 'C'])
        self.assertNotIn('A', cleaned_df.columns)
        self.assertNotIn('C', cleaned_df.columns)

    def test_clean_dataframe_columns_rename(self):
        '''
        Testa se as colunas são renomeadas corretamente
        '''
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
        cleaned_df = clean_dataframe(df, columns_to_rename={'A': 'X', 'B': 'Y'})
        self.assertNotIn('A', cleaned_df.columns)
        self.assertIn('X', cleaned_df.columns)
        self.assertIn('Y', cleaned_df.columns)

    def test_clean_dataframe_numeric_columns(self):
        '''
        Testa se as colunas são convertidas corretamente para tipo numérico
        '''
        df = pd.DataFrame({'A': ['1', '2', '3'], 'B': ['4', '5', '6'], 'C': [7, 8, 9]})
        cleaned_df = clean_dataframe(df, numeric_columns=['A', 'B'])
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['A']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['B']))

    def test_clean_dataframe_drop_na(self):
        '''
        Testa se as linhas com valores NaN são removidas corretamente
        '''
        df = pd.DataFrame({'A': [1, 2, None], 'B': [4, 5, 6], 'C': [7, None, 9]})
        cleaned_df = clean_dataframe(df, drop_na=True)
        self.assertEqual(len(cleaned_df), 1)


if __name__ == '__main__':
    unittest.main()