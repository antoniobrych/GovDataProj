import unittest
from utils_henrique import take_data, transform_column
import pandas as pd

class EmptyFileError(Exception):
    pass

class NonexistentColumnsError(Exception):
    pass

class TestTakeDataFunction(unittest.TestCase):

    def test_take_data_with_empty_file(self):
        csv_file = 'empty.csv'
        with open(csv_file, 'w') as f:
            f.write('')
        with self.assertRaises(EmptyFileError):
            take_data(csv_file, ['Nome'])

    def test_take_data_with_nonexistent_columns(self):
        csv_file = 'data.csv'
        with open(csv_file, 'w') as f:
            f.write('Nome\nAlice\nBob\nCharlie')
        with self.assertRaises(NonexistentColumnsError):
            take_data(csv_file, ['Salário', 'Cargo'])

    def test_take_data_with_valid_data(self):
        csv_file = 'data.csv'
        with open(csv_file, 'w') as f:
            f.write('Nome\nAlice\nBob\nCharlie')
        result = take_data(csv_file, ['Nome'])
        expected = pd.DataFrame({'Nome': ['Alice', 'Bob', 'Charlie']})
        pd.testing.assert_frame_equal(result, expected)

    def test_take_data_with_invalid_format(self):
        csv_file = 'invalid.csv'
        with open(csv_file, 'w') as f:
            f.write('Nome;Idade;Cidade\nAlice;25;São Paulo\nBob;30;Rio de Janeiro')
        with self.assertRaises(ValueError):
            take_data(csv_file, ['Nome'])


class TestTransformColumnFunction(unittest.TestCase):

    def test_transform_column_with_valid_data(self):
        data = {'ESCOLARIDADE': ['Ensino Fundamental', 'Ensino Médio', 'Ensino Superior', 'Mestrado']}
        df = pd.DataFrame(data)
        transform_dict = {'Ensino Fundamental': 'Fundamental', 'Ensino Médio': 'Médio', 'Ensino Superior': 'Superior'}
        result = transform_column(df, 'ESCOLARIDADE', transform_dict)
        expected = pd.DataFrame({'ESCOLARIDADE': ['Fundamental', 'Médio', 'Superior', 'Mestrado']})
        pd.testing.assert_frame_equal(result, expected)

    def test_transform_column_with_nonexistent_column(self):
        df = pd.read_csv("sermil2022.csv")
        with self.assertRaises(KeyError):
            transform_column(df, "importante", {"importante": "urgente"})

    def test_transform_column_with_empty_data(self):
        df = pd.DataFrame({'NOME': []})
        transform_dict = {}
        result = transform_column(df, 'NOME', transform_dict)
        expected = pd.DataFrame({'NOME': []})
        pd.testing.assert_frame_equal(result, expected)

if __name__ == '__main__':
    unittest.main()

