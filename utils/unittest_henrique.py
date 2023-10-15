import unittest
from .utils_henrique import take_data, transform_column, EmptyFileError, NonexistentColumnsError
import pandas as pd

class TestTakeDataFunction(unittest.TestCase):
    def test_take_data_with_empty_file(self):
        csv_file = 'arquivo_vazio.csv'
        try:
            take_data(csv_file, ['Nome'])
        except Exception as e:
            pass

    def test_take_data_with_valid_data(self):
        csv_file = 'data.csv'
        with open(csv_file, 'w') as f:
            f.write('Nome\nAlice\nBob\nCharlie')
        result = take_data(csv_file, ['Nome'])
        expected = pd.DataFrame({'Nome': ['Alice', 'Bob', 'Charlie']})
        pd.testing.assert_frame_equal(result, expected)

    def test_take_data_with_invalid_format(self):
        csv_file = 'arquivo_invalido.csv' 
        try:
            take_data(csv_file, ['Nome'])
        except Exception as e:
            pass

class TestTransformColumnFunction(unittest.TestCase):
    def test_transform_column_with_valid_data(self):
        data = {'ESCOLARIDADE': ['Ensino Fundamental', 'Ensino Médio', 'Ensino Superior', 'Mestrado']}
        df = pd.DataFrame(data)
        transform_dict = {'Ensino Fundamental': 'Fundamental', 'Ensino Médio': 'Médio', 'Ensino Superior': 'Superior'}
        result = transform_column(df, 'ESCOLARIDADE', transform_dict)
        expected = pd.DataFrame({'ESCOLARIDADE': ['Fundamental', 'Médio', 'Superior', 'Mestrado']})
        pd.testing.assert_frame_equal(result, expected)

    def test_transform_column_with_nonexistent_column(self):
        df = pd.read_csv("sermil2022.csv")  # Substitua pelo caminho correto
        with self.assertRaises(KeyError):
            transform_column(df, "Salário", {"Salário": "Rendimento"})


    def test_transform_column_with_empty_data(self):
        df = pd.DataFrame({'NOME': []})
        transform_dict = {}
        result = transform_column(df, 'NOME', transform_dict)
        expected = pd.DataFrame({'NOME': []})
        pd.testing.assert_frame_equal(result, expected)

if __name__ == '__main__':
    unittest.main()
