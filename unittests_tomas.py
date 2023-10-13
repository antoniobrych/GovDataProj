import unittest
import importlib
import pandas as pd
from utils_tomas import get_age, get_state_coordinates, merge_height_geography_df,create_height_heatmap,get_stats,create_correlation_matrix,create_age_histogram,check_libraries


class TestMergeData(unittest.TestCase):
    """
    Classe de teste para a função merge_height_geography_df
    """
    def setUp(self):
        """
        Prepara os dados necessários para os testes
        Carrega o DataFrame 'df_1' do arquivo 'sermil2022.csv'
        Obtém o DataFrame 'df_2' com as coordenadas dos estados
        """
        self.df_1 = pd.read_csv('sermil2022.csv')
        self.df_2 = get_state_coordinates('bcim_2016_21_11_2018.gpkg', True)

    def test_merge_data_correct(self):
        """
        Teste com a função merge entre dois dataframes
        Verifica se a função produz um resultado não vazio
        """
        result = merge_height_geography_df(self.df_1, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertFalse(result.empty)

    def test_height_values_not_numeric(self):
        """
        Teste com a função merge passando valores não numéricos
        Verifica se a função retorna None quando 'ALTURA' contém valores não numéricos
        """
        test_df = self.df_1.copy()
        test_df['ALTURA'] = test_df['ALTURA'].astype(str)
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertIsNone(result)

    def test_height_values_zeros(self):
        """
        Teste com a função merge passando valores nulos para a coluna das Alturas
        Verifica se a função retorna None quando 'ALTURA' contém valores iguais a zero
        """
        test_df = self.df_1.copy()
        test_df.loc[0,'ALTURA'] = 0
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertIsNone(result)

    def test_height_values_negative(self):
        """
        Teste com a função merge passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando 'ALTURA' contém valores negativos
        """
        test_df = self.df_1.copy()
        test_df.loc[0,'ALTURA'] = -19
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertIsNone(result)

    def test__state_column_existence(self):
        """
        Teste com a função merge passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando a coluna 'UF_RESIDENCIA' é renomeada
        """
        test_df = self.df_1.copy()
        test_df.rename({"UF_RESIDENCIA": "Siglas"},axis=1, inplace=True)
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertIsNone(result)

    def test__height_column_existence(self):
        """
        Teste com a função merge passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando a coluna 'ALTURA' é renomeada
        """
        test_df = self.df_1.copy()
        test_df.rename({"ALTURA": "Tamanho"},axis=1, inplace=True)
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
        Carrega o DataFrame 'df_1' a partir do arquivo 'sermil2022.csv'
        Obtém o DataFrame 'df_2' com as coordenadas dos estados
        Realiza a mesclagem de dados no DataFrame 'df_3'
        """
        self.df_1 = pd.read_csv('sermil2022.csv')
        self.df_2 = get_state_coordinates('bcim_2016_21_11_2018.gpkg', True)
        self.df_3 = merge_height_geography_df(self.df_1,'ALTURA','UF_RESIDENCIA',self.df_2)

    def test_heatmap_correct(self):
        """
        Teste com a função merge entre dois dataframes
        Verifica se a função produz um resultado válido
        """
        result = create_height_heatmap(self.df_3, 'ALTURA', 'UF_RESIDENCIA')
        self.assertTrue(result)

    def test_height_values_zeros(self):
        """
        Teste com a função merge passando valores nulos para a coluna das Alturas
        Verifica se a função retorna None quando 'ALTURA' contém valores iguais a zero
        """
        test_df = self.df_3.copy()
        test_df.loc[0,"ALTURA"] = 0
        result = create_height_heatmap(test_df,'ALTURA','UF_RESIDENCIA')
        self.assertIsNone(result)

    def test_height_values_negative(self):
        """
        Teste com a função merge passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando 'ALTURA' contém valores negativos
        """
        test_df = self.df_3.copy()
        test_df.loc[0,"ALTURA"] = -19
        result = create_height_heatmap(test_df,'ALTURA','UF_RESIDENCIA')
        self.assertIsNone(result)

    def test_state_column_existence(self):
        """
        Teste com a função merge passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando a coluna 'UF_RESIDENCIA' é renomeada
        """
        test_df = self.df_3.copy()
        test_df.rename({"UF_RESIDENCIA": "Siglas"},axis=1, inplace=True)
        result = create_height_heatmap(test_df,'ALTURA','UF_RESIDENCIA')
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
        Carrega o DataFrame 'df_1' do arquivo 'sermil2022.csv'
        """
        self.df_1 = pd.read_csv('sermil2022.csv')

    def test_get_stats_data_correct(self):
        """
        Teste com a função que retorna um pd.Series
        Verifica se a função retorna um pd.Series válido
        """
        result = get_stats(self.df_1, 'ALTURA')
        self.assertFalse(result.empty)

    def test_numeric_values_zeros(self):
        """
        Teste com a função, passando valores nulos para a coluna das Alturas
        Verifica se a função retorna None quando 'CINTURA' contém valores iguais a zero
        """
        test_df = self.df_1.copy()
        test_df.loc[0,"CINTURA"] = 0
        result = get_stats(test_df,'CINTURA')
        self.assertIsNone(result)

    def test_numeric_values_negative(self):
        """
        Teste com a função, passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando 'CABECA' contém valores negativos
        """
        test_df = self.df_1.copy()
        test_df.loc[0,"CABECA"] = -19
        result = get_stats(test_df,'CABECA')
        self.assertIsNone(result)

    def test_missing_column(self):
        """
        Teste com uma coluna inexistente no DataFrame
        Verifica se a função gera uma exceção KeyError quando a coluna não existe.
        """
        with self.assertRaises(KeyError):
            get_stats(self.df_1, 'COLUNA_INEXISTENTE')
class TestCorrelationMatrixCreation(unittest.TestCase):
    """
    Classe de teste para a função create_correlation_matrix
    """
    def setUp(self):
        """
        Prepara os dados necessários para os testes
        Carrega o DataFrame 'df_1' a partir do arquivo 'sermil2022.csv'
        """
        self.df_1 = pd.read_csv('sermil2022.csv')

    def test_corrmatrix_correct(self):
        """
        Teste com a função merge entre dois dataframes
        Verifica se a função produz uma matriz de correlação válida
        """
        result = create_correlation_matrix(self.df_1,['ALTURA','CINTURA','CABECA','CALCADO'])
        self.assertTrue(result)

    def test_height_values_zeros(self):
        """
        Teste com a função merge passando valores nulos para a coluna das Alturas
        Verifica se a função retorna None quando 'ALTURA' contém valores iguais a zero
        """
        test_df = self.df_1.copy()
        test_df.loc[0,"ALTURA"] = 0
        result = create_correlation_matrix(test_df,'ALTURA')
        self.assertIsNone(result)

    def test_height_values_negative(self):
        """
        Teste com a função merge passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando 'CINTURA' contém valores negativos
        """
        test_df = self.df_1.copy()
        test_df.loc[0,"CINTURA"] = -19
        result = create_correlation_matrix(test_df,['ALTURA','CINTURA'])
        self.assertIsNone(result)

    def test_column_existence(self):
        """
        Teste com a função merge passando valores negativos para a coluna das Alturas
        Verifica se a função retorna None quando a coluna 'ALTURA' é renomeada
        """
        test_df = self.df_1.copy()
        test_df.rename({"ALTURA": "tamanho"},axis=1, inplace=True)
        result = create_correlation_matrix(test_df,['ALTURA','CINTURA'])
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
        Carrega o DataFrame 'df_1' a partir do arquivo 'sermil2022.csv'
        """
        self.df_1 = pd.read_csv('sermil2022.csv')

    def test_get_stats_data_correct(self):
        """
        Teste com a função que retorna um pd.Series
        Verifica se a função retorna um pd.Series válido
        """
        result = get_age(self.df_1, 'ANO_NASCIMENTO')
        self.assertFalse(result.empty)

    def test_numeric_small_values(self):
        """
        Teste com a função, passando valores pequenos para a coluna 'ANO_NASCIMENTO'
        Verifica se a função retorna None quando 'ANO_NASCIMENTO' contém valores pequenos
        """
        test_df = self.df_1.copy()
        test_df.loc[0,"ANO_NASCIMENTO"] = 1900
        result = get_age(test_df,'ANO_NASCIMENTO')
        self.assertIsNone(result)

    def test_column_existence(self):
        """
        Teste com a função, passando valores negativos para a coluna 'ANO_RESIDENCIA'
        Verifica se a função retorna None quando a coluna 'ANO_RESIDENCIA' é renomeada
        """
        test_df = self.df_1.copy()
        test_df.rename({"ANO_RESIDENCIA": "Data_nascimento"},axis=1, inplace=True)
        result = get_age(test_df,'ANO_RESIDENCIA')
        self.assertIsNone(result)

    def tearDown(self):
        pass

class TestAgeHistogramCreation():
    """
    Classe de teste para a função create_age_histogram
    """
    def setUp(self):
        """
        Prepara os dados necessários para os testes.
        Carrega o DataFrame 'df_1' a partir do arquivo 'sermil2022.csv'
        Obtém o DataFrame 'df_2' com idades calculadas a partir do ano de nascimento
        """
        self.df_1 = pd.read_csv('sermil2022.csv')
        self.df_2 = get_age(self.df_1,'ANO_NASCIMENTO')

    def test_agehist_correct(self):
        """
        Teste com a função create_age_histogram
        Verifica se a função produz um histograma de idades válido
        """
        result = create_age_histogram(self.df_2)
        self.assertTrue(result)

    def test_column_existence(self):
        """
        Teste com a função create_age_histogram, renomeando a coluna 'IDADE'
        Verifica se a função retorna None quando a coluna 'IDADE' é renomeada
        """
        test_df = self.df_2.copy()
        test_df.rename({"IDADE": "Age"},axis=1, inplace=True)
        result = create_age_histogram(test_df,'IDADE')
        self.assertIsNone(result)

    def test_age_values_zeros(self):
        """
        Teste com a função create_age_histogram, passando valores nulos para a coluna 'IDADE'
        Verifica se a função retorna None quando a coluna 'IDADE' contém valores iguais a zero
        """
        test_df = self.df_2.copy()
        test_df.loc[0,"IDADE"] = 0
        result = create_age_histogram(test_df,'IDADE')
        self.assertIsNone(result)

    def test_age_values_negative(self):
        """
        Teste com a função create_age_histogram, passando valores negativos para a coluna 'IDADE'
        Verifica se a função retorna None quando a coluna 'IDADE' contém valores negativos
        """
        test_df = self.df_2.copy()
        test_df.loc[0,"IDADE"] = -19
        result = create_age_histogram(test_df,'IDADE')
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
