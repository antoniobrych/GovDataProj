from cleandata import make_http_request
from downloaddata import download_csv_local
import unittest
import os

class TestMakeHttpRequest(unittest.TestCase):
    '''
    Classe de teste para a função make_https_request.
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
        Defina a URL de teste e o caminho local do arquivo.
        '''
        self.test_url = 'https://dadosabertos.eb.mil.br/arquivos/sermil/sermil2022.csv'
        self.local_file_path = 'test_data.csv'

    def tearDown(self):
        '''
        Exclua o arquivo CSV de teste se ele existir.
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


if __name__ == '__main__':
    unittest.main()