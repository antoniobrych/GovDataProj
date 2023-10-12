import unittest
import pandas as pd

from analysis_utils import yearly_mean

class TestYearlyMeanFunction(unittest.TestCase):
    
    def setUp(self):
        # Creating dummy dataframe
        data = {
            'VINCULACAO_ANO': [2007, 2007, 2008, 2008, 2009],
            'CINTURA': [80.0, 80.2, 79.9, 80.1, 80.3],
            'PESO': [70.0, 70.2, 70.3, 70.5, 70.7],
            'ALTURA': [170.0, 170.2, 170.3, 170.5, 170.7],
            'CABECA': [56.0, 56.2, 56.3, 56.5, 56.7]
        }
        self.test_df = pd.DataFrame(data)

    def test_yearly_mean_calculation(self):
        # Test if function calculate yearly means correctly
        result_df = yearly_mean(self.test_df)
        expected_means = {
            2007: (80.1, 70.1, 170.1, 56.1),
            2008: (80.0, 70.4, 170.4, 56.4),
            2009: (80.3, 70.7, 170.7, 56.7)
        }
        for year, means in expected_means.items():
            self.assertTrue(year in result_df.index)
            for col, expected_mean in zip(result_df.columns, means):
                self.assertAlmostEqual(result_df.loc[year, col], expected_mean, places=2)

    def test_no_nan_values(self):
        # Test if the function can handle NaN values correctly
        data = {
            'VINCULACAO_ANO': [2007, 2008, 2009],
            'CINTURA': [80.0, None, 79.9],
            'PESO': [70.0, 70.3, None],
            'ALTURA': [170.0, 170.3, 179.5],
            'CABECA': [56.0,56.3,57.6]
        }
        test_df = pd.DataFrame(data)
        result_df = yearly_mean(test_df)
        print(result_df)
        self.assertEqual(len(result_df), 1)  # One year expected

if __name__ == '__main__':
    unittest.main()
