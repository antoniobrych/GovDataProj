import unittest
import pandas as pd
from utils_tomas import get_age, get_state_coordinates, merge_height_geography_df,create_height_heatmap

class TestMergeData(unittest.TestCase):
    '''
    Classe de teste para a funcao merge_height_geography_df
    '''
    def setUp(self):
        self.df_1 = pd.read_csv('sermil2022.csv')
        self.df_2 = get_state_coordinates('bcim_2016_21_11_2018.gpkg', True)

    def test_merge_data_correct(self):
        '''
        Teste com a funcao merge entre dois dataframes
        '''
        result = merge_height_geography_df(self.df_1, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertFalse(result.empty)

    def test_height_values_not_numeric(self):
        '''
        Teste com a funcao merge passando valores não númericos
        '''
        test_df = self.df_1.copy()
        test_df['ALTURA'] = test_df['ALTURA'].astype(str)
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertIsNone(result)

    def test_height_values_zeros(self):
        '''
        Teste com a funcao merge passando valores nulos para a coluna das Alturas
        '''
        test_df = self.df_1.copy()
        test_df.loc[0,'ALTURA'] = 0
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertIsNone(result)

    def test_height_values_negative(self):
        '''
        Teste com a funcao merge passando valores negativos para a coluna das Alturas
        '''
        test_df = self.df_1.copy()
        test_df.loc[0,'ALTURA'] = -19
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertIsNone(result)

    def test__state_column_existence(self):
        '''
        Teste com a funcao merge passando valores negativos para a coluna das Alturas
        '''
        test_df = self.df_1.copy()
        test_df.rename({"UF_RESIDENCIA": "Siglas"},axis=1, inplace=True)
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertIsNone(result)

    def test__height_column_existence(self):
        '''
        Teste com a funcao merge passando valores negativos para a coluna das Alturas
        '''
        test_df = self.df_1.copy()
        test_df.rename({"ALTURA": "Tamanho"},axis=1, inplace=True)
        result = merge_height_geography_df(test_df, 'ALTURA', 'UF_RESIDENCIA', self.df_2)
        self.assertIsNone(result)

    def tearDown(self):
        # Não sei oq escrever aqui
        pass

class TestMapHeatmap(unittest.TestCase):
    '''
    Classe de teste para a funcao create_height_heatmap
    '''
    def setUp(self):
        self.df_1 = pd.read_csv('sermil2022.csv')
        self.df_2 = get_state_coordinates('bcim_2016_21_11_2018.gpkg', True)
        self.df_3 = merge_height_geography_df(self.df_1,'ALTURA','UF_RESIDENCIA',self.df_2)

    def test_height_values_zeros(self):
        '''
        Teste com a funcao merge passando valores nulos para a coluna das Alturas
        '''
        test_df = self.df_3.copy()
        test_df.loc[0,"ALTURA"] = 0
        result = create_height_heatmap(test_df)
        self.assertIsNone(result)

    def test_height_values_negative(self):
        '''
        Teste com a funcao merge passando valores negativos para a coluna das Alturas
        '''
        test_df = self.df_3.copy()
        test_df.loc[0,"ALTURA"] = -19
        result = create_height_heatmap(test_df)
        self.assertIsNone(result)

    def test_column_existence(self):
        '''
        Teste com a funcao merge passando valores negativos para a coluna das Alturas
        '''
        test_df = self.df_3.copy()
        test_df.rename({"UF_RESIDENCIA": "Siglas"},axis=1, inplace=True)
        result = create_height_heatmap(test_df)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

print(TestMapHeatmap.setUp())