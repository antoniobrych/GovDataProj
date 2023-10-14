import unittest
import pandas as pd
import os
from data_utils import concatenate_last_n_csv_files, integrity_check

class TestDataUtils(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        # Best practises, to avoid messing with the original files

        self.test_dir = 'test_data'
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        # Remove the temporary directory and its contents
        # Cleaning up.
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.test_dir)

    def test_concatenate_last_n_csv_files(self):
        # Create some dummy dataset
        # Inserting those files
        for i in range(2012,2023,1):
            file_name = f'sermil{i}.csv'
            data = pd.DataFrame({'A': [i], 'B': [i * 2]})
            data.to_csv(os.path.join(self.test_dir, file_name), index=False)

        # Test concatenation with n=5
        result = concatenate_last_n_csv_files(self.test_dir, self.test_dir, n=5)
        print(result)
        self.assertEqual(result.shape[0], 6)  # Check the number of rows in the concatenated DataFrame

    def test_integrity_check(self):
        # Create some test CSV files
        for year in range(2012, 2023):
            file_name = f'sermil{year}.csv'
            open(os.path.join(self.test_dir, file_name), 'w').close()

        # Test integrity with the correct range
        integrity_result = integrity_check(self.test_dir, begin=2012, end=2022)
        self.assertTrue(integrity_result)

        # Test integrity with a missing file
        os.remove(os.path.join(self.test_dir, 'sermil2015.csv'))
        integrity_result = integrity_check(self.test_dir, begin=2012, end=2022)
        self.assertFalse(integrity_result)

if __name__ == '__main__':
    #Running Unittests
    unittest.main()
