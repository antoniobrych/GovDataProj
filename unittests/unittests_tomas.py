import sys

# Importante: mudar o path de acordo com a sua máquina, observe que é o path para a pasta utils.
sys.path.append('C:/Users/B51095/GovDataProj/utils')

import unittest
import os
import pandas as pd

# Adicionar um ponto antes do nome do módulo causa um erro na minha máquina quando executo o código.
from utils_tomas import get_age,  merge_height_geography_df, create_height_heatmap, get_stats, create_correlation_matrix, create_age_histogram, get_state_coordinates
from download_data_tomas import check_libraries, download_gpkg_local

class TestExistenceFile(unittest.TestCase):

    def setUp(self):
        """
        Prepara a URL necessária para os testes
        """
        self.local_file_path = "data/geo_data.gpkg"

    def test_file_is_local(self):
        """
        Testa se o arquivo está presente localmente.
        """
        # Verifica se o arquivo local existe.
        if os.path.exists(self.local_file_path):
            self.assertTrue(True)  # Se o arquivo existe, o teste é bem-sucedido.
        else:
            self.fail("O arquivo GeoPackage não foi baixado localmente")  # Teste falha com uma mensagem de erro.

    def test_fake_url(self):
        """
        Teste com uma URL inexistente
        """
        # Arquivo de uma URL inexistente.
        result = download_gpkg_local("URL_INEXISTENTE.com")
        self.assertIsNone(result)  # Verifica se o resultado é None, pra ver se resultou em um download mal-sucedido.



class TestMergeData(unittest.TestCase):
    """
    Classe de teste para a função merge_height_geography_df
    """

    def setUp(self):
        """
        Prepara os dados necessários para os testes
        Carrega o DataFrame 'df_1' do arquivo "data/sermil2022.csv"
        Obtém o DataFrame 'df_2' com as coordenadas dos estados
        """
        self.df_1 = pd.read_csv("data/sermil2022.csv")
        
        self.df_2 = get_state_coordinates("data/geo_data.gpkg", True)

    def test_merge_data_correct(self):
        """
        Teste com a função merge entre dois dataframes
        Verifica se a função produz um resultado não vazio
        """
        # Realiza o merge dos dfs com dada a função 'merge_height_geography_df'.
        result = merge_height_geography_df(self.df_1, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        
        # Verifica se o resultado não está vazio.
        self.assertFalse(result.empty)

    def test_height_values_not_numeric(self):
        """
        Teste com a função merge passando valores não numéricos
        Verifica se a função retorna None quando 'ALTURA' contém valores não numéricos
        """
        # Cria uma cópia do DataFrame 'df_1' e converte a coluna 'ALTURA' pra str.
        test_df = self.df_1.copy()
        test_df['ALTURA'] = test_df['ALTURA'].astype(str)
        
        # Realiza o merge de dataframes com a função 'merge_height_geography_df' usando valores (str) da coluna 'ALTURA'.
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        
        # Verifica se o a função funcionou corretamente para valores não numéricos.
        self.assertIsNone(result)


    def test_height_values_zeros(self):
        """
        Teste com a função merge passando valores nulos para a coluna das Alturas
        Verifica se a função retorna None quando 'ALTURA' contém valores iguais a zero
        """
        test_df = self.df_1.copy()
        test_df.loc[0, 'ALTURA'] = 0
        
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        
        # Verifica se a função tratou corretamente valores iguais a zero.
        self.assertIsNone(result)

    def test_height_values_negative(self):
        """
        Teste com a função merge passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando 'ALTURA' contém valores negativos
        """
        # Cria uma cópia do DataFrame 'df_1' e define o valor da primeira linha da coluna 'ALTURA' como negativo.
        test_df = self.df_1.copy()
        test_df.loc[0, 'ALTURA'] = -19
        
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        
        # Verifica se o a função tratou corretamente valores negativos.
        self.assertIsNone(result)

    def test_state_column_existence(self):
        """
        Teste com a função merge quando a coluna 'UF_RESIDENCIA' é renomeada
        Verifica se a função retorna None quando a coluna 'UF_RESIDENCIA' é renomeada
        """
        # Cria uma cópia do DataFrame 'df_1' e renomeia a coluna 'UF_RESIDENCIA' como 'Siglas'.
        test_df = self.df_1.copy()
        test_df.rename({"UF_RESIDENCIA": "Siglas"}, axis=1, inplace=True)
        
        # Realiza o merge dos dfs com 'merge_height_geography_df' usando a coluna renomeada 'Siglas'.
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        
        # Verifica se a função tratou corretamente a renomeação da coluna.
        self.assertIsNone(result)

    def test_height_column_existence(self):
        """
        Teste com a função merge quando a coluna 'ALTURA' é renomeada
        Verifica se a função retorna None quando a coluna 'ALTURA' é renomeada
        """
        test_df = self.df_1.copy()
        test_df.rename({"ALTURA": "Tamanho"}, axis=1, inplace=True)
        
        # Realiza o merge dos dfs com a função 'merge_height_geography_df' usando a coluna 'Tamanho'.
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        
        self.assertIsNone(result)

    def tearDown(self):
        pass


class TestMapHeatmapCreation(unittest.TestCase):
    """
    Classe de teste para a função create_height_heatmap
    """

    def setUp(self):
        """
        Carrega o DataFrame 'df_1' a partir do arquivo "data/sermil2022.csv"
        Obtém o DataFrame 'df_2' com as coordenadas dos estados
        Realiza o merge de dados no DataFrame 'df_3'
        """
        # Carrega o DataFrame 'df_1' a partir do arquivo CSV "sermil2022.csv" no diretório "data".
        self.df_1 = pd.read_csv("data/sermil2022.csv")
        
        self.df_2 = get_state_coordinates("data/geo_data.gpkg", True)
        
        self.df_3 = merge_height_geography_df(self.df_1, 'ALTURA', 'UF_RESIDENCIA', self.df_2)

    def test_heatmap_correct(self):
        """
        Teste com a função create_height_heatmap
        Verifica se a função produz um resultado válido
        """
        # Chama a função 'create_height_heatmap' com o DataFrame 'df_3' e colunas 'ALTURA' e 'UF_RESIDENCIA'.
        result = create_height_heatmap(self.df_3, 'ALTURA', 'UF_RESIDENCIA')
        
        # Verifica se o resultado é válido (não nulo ou vazio).
        self.assertTrue(result)

    def test_height_values_zeros(self):
        """
        Teste com a função create_height_heatmap passando valores iguais a zero para a coluna das Alturas
        Verifica se a função retorna None quando 'ALTURA' contém valores iguais a zero
        """
        # Cria uma cópia do DataFrame 'df_3' e define o valor da primeira linha da coluna 'ALTURA' como zero.
        test_df = self.df_3.copy()
        test_df.loc[0, "ALTURA"] = 0
        
        # Chama a função 'create_height_heatmap' com o DataFrame modificado, onde 'ALTURA' contém valores iguais a zero.
        result = create_height_heatmap(test_df, 'ALTURA', 'UF_RESIDENCIA')
        
        self.assertIsNone(result)

    def test_height_values_negative(self):
        """
        Teste com a função create_height_heatmap passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando 'ALTURA' contém valores negativos
        """
        # Cria uma cópia do DataFrame 'df_3' e define o valor da primeira linha da coluna 'ALTURA' como negativo.
        test_df = self.df_3.copy()
        test_df.loc[0, "ALTURA"] = -19
        
        # Chama a função 'create_height_heatmap' com o DataFrame modificado, em que a coluna 'ALTURA' tem valores negativos.
        result = create_height_heatmap(test_df, 'ALTURA', 'UF_RESIDENCIA')
        
        # Verifica se a função tratou corretamente valores negativos.
        self.assertIsNone(result)

    def test_state_column_existence(self):
        """
        Teste com a função create_height_heatmap quando a coluna 'UF_RESIDENCIA' é renomeada
        Verifica se a função retorna None quando a coluna 'UF_RESIDENCIA' é renomeada
        """
        # Cria uma cópia do DataFrame 'df_3' e renomeia a coluna 'UF_RESIDENCIA' como 'Siglas'.
        test_df = self.df_3.copy()
        test_df.rename({"UF_RESIDENCIA": "Siglas"}, axis=1, inplace=True)
        
        # Chama a função 'create_height_heatmap' com o DataFrame modificado, onde a coluna 'UF_RESIDENCIA' foi renomeada.
        result = create_height_heatmap(test_df, 'ALTURA', 'UF_RESIDENCIA')
        
        self.assertIsNone(result)

    def tearDown(self):
        pass



class TestGetStats(unittest.TestCase):
    """
    Classe de teste para a função get_stats
    """

    def setUp(self):
        """
        Prepara os dados necessários para os testes
        Carrega o DataFrame 'df_1' do arquivo "data/sermil2022.csv"
        """
        self.df_1 = pd.read_csv("data/sermil2022.csv")

    def test_get_stats_data_correct(self):
        """
        Teste com a função que retorna um pd.Series
        Verifica se a função retorna um pd.Series válido
        """
        result = get_stats(self.df_1, 'ALTURA')
        
        # Verifica se o resultado é um pd.Series não vazio.
        self.assertFalse(result.empty)

    def test_numeric_values_zeros(self):
        """
        Teste com a função, passando valores nulos para a coluna das Alturas
        Verifica se a função retorna None quando 'CINTURA' contém valores iguais a zero
        """
        test_df = self.df_1.copy()
        test_df.loc[0, "CINTURA"] = 0
        
        # Chama a função 'get_stats' com o DataFrame modificado, onde 'CINTURA' contém valores iguais a zero.
        result = get_stats(test_df, 'CINTURA')
        
        # Verifica se a função tratou corretamente valores iguais a zero.
        self.assertIsNone(result)

    def test_numeric_values_negative(self):
        """
        Teste com a função, passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando 'CABECA' contém valores negativos
        """
        test_df = self.df_1.copy()
        test_df.loc[0, "CABECA"] = -19
        
        # Chama a função 'get_stats' com o DataFrame modificado, onde 'CABECA' tem valores negativos.
        result = get_stats(test_df, 'CABECA')
        
        # Verifica se o resultado é None, indicando que a função tratou corretamente valores negativos.
        self.assertIsNone(result)

    def test_missing_column(self):
        """
        Teste com uma coluna inexistente no DataFrame
        Verifica se a função gera uma exceção KeyError quando a coluna não existe.
        """
        # Tenta chamar a função 'get_stats' com uma coluna inexistente.
        with self.assertRaises(KeyError):
            get_stats(self.df_1, 'COLUNA_INEXISTENTE')


class TestCorrelationMatrixCreation(unittest.TestCase):
    """
    Classe de teste para a função create_correlation_matrix
    """

    def setUp(self):
        """
        Prepara os dados necessários para os testes
        Carrega o DataFrame 'df_1' a partir do arquivo "data/sermil2022.csv"
        """
        # Carrega o DataFrame 'df_1' a partir do arquivo CSV "sermil2022.csv" no diretório "data".
        self.df_1 = pd.read_csv("data/sermil2022.csv")

    def test_corrmatrix_correct(self):
        """
        Teste com a função create_correlation_matrix
        Verifica se a função produz uma matriz de correlação válida
        """
        result = create_correlation_matrix(self.df_1, ['ALTURA', 'CINTURA', 'CABECA', 'CALCADO'])
        
        self.assertTrue(result)

    def test_height_values_zeros(self):
        """
        Teste com a função create_correlation_matrix passando valores iguais a zero para a coluna das Alturas
        Verifica se a função retorna None quando 'ALTURA' contém valores iguais a zero
        """
        test_df = self.df_1.copy()
        test_df.loc[0, "ALTURA"] = 0
        
        # Chama a função 'create_correlation_matrix' com o DataFrame modificado, onde 'ALTURA' contém valores iguais a zero.
        result = create_correlation_matrix(test_df, 'ALTURA')
        
        # Verifica se a função tratou corretamente valores iguais a zero.
        self.assertIsNone(result)

    def test_height_values_negative(self):
        """
        Teste com a função create_correlation_matrix passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando 'CINTURA' contém valores negativos
        """
        # Cria uma cópia do DataFrame 'df_1' e define o valor da primeira linha da coluna 'CINTURA' como negativo.
        test_df = self.df_1.copy()
        test_df.loc[0, "CINTURA"] = -19
        
        # Chama a função 'create_correlation_matrix' com o DataFrame modificado, onde 'CINTURA' contém valores negativos.
        result = create_correlation_matrix(test_df, ['ALTURA', 'CINTURA'])
        
        self.assertIsNone(result)

    def test_column_existence(self):
        """
        Teste com a função create_correlation_matrix quando a coluna 'ALTURA' é renomeada
        Verifica se a função retorna None quando a coluna 'ALTURA' é renomeada
        """
        # Cria uma cópia do DataFrame 'df_1' e renomeia a coluna 'ALTURA' como 'tamanho'.
        test_df = self.df_1.copy()
        test_df.rename({"ALTURA": "tamanho"}, axis=1, inplace=True)
        
        # Chama a função 'create_correlation_matrix' com o DataFrame modificado.
        result = create_correlation_matrix(test_df, ['ALTURA', 'CINTURA'])
        
        # Verifica se a função tratou corretamente a renomeação da coluna.
        self.assertIsNone(result)

    def tearDown(self):
        pass

class TestGetAge(unittest.TestCase):
    '''
    Classe de teste para a função get_age
    '''

    def setUp(self):
        """
        Prepara os dados necessários para os testes
        Carrega o DataFrame 'df_1' a partir do arquivo "data/sermil2022.csv"
        """
        self.df_1 = pd.read_csv("data/sermil2022.csv")

    def test_get_stats_data_correct(self):
        """
        Teste com a função que retorna um pd.Series
        Verifica se a função retorna um pd.Series válido
        """
        result = get_age(self.df_1, 'ANO_NASCIMENTO')
        
        # Verifica se o resultado é um pd.Series válido (não está vazio).
        self.assertFalse(result.empty)

    def test_numeric_small_values(self):
        """
        Teste com a função, passando valores pequenos para a coluna 'ANO_NASCIMENTO'
        Verifica se a função retorna None quando 'ANO_NASCIMENTO' contém valores pequenos
        """
        test_df = self.df_1.copy()
        test_df.loc[0, "ANO_NASCIMENTO"] = 1900
        
        # Chama a função 'get_age' com o DataFrame modificado, onde 'ANO_NASCIMENTO' contém valores pequenos.
        result = get_age(test_df, 'ANO_NASCIMENTO')
        
        # Verifica se o resultado é None, indicando que a função tratou corretamente valores pequenos.
        self.assertIsNone(result)

    def test_column_existence(self):
        """
        Teste com a função, passando valores negativos para a coluna 'ANO_RESIDENCIA'
        Verifica se a função retorna None quando a coluna 'ANO_RESIDENCIA' é renomeada
        """
        test_df = self.df_1.copy()
        test_df.rename({"ANO_RESIDENCIA": "Data_nascimento"}, axis=1, inplace=True)
        
        # Chama a função 'get_age' com o DataFrame modificado.
        result = get_age(test_df, 'ANO_RESIDENCIA')
        
        self.assertIsNone(result)

    def tearDown(self):
        pass


class TestCheckLibraries(unittest.TestCase):
    """
    Testa se o usuário possui todas as bilbiotecas necessárias instaladas para rodar o programa.
    """

    def test_check_libraries(self):
        missing_libraries = check_libraries()
        self.assertIsNone(missing_libraries)


if __name__ == '__main__':
    unittest.main()
