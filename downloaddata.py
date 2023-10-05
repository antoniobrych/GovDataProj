from cleandata import process_data,make_http_request
from typing import List

def download_csv_local(url: str, local_file:str = None ,columns: List[str] = None):
    '''
    Serve para baixar o CSV localmente de uma URL.
    Permite que você baixe colunas selecionadas, ou
    seja, não baixe todo o csv.

    Parameters
    ----------
    url : str
        A URL que aponta para o conjunto de dados a ser lido.
    
    local_file : str, optional
        Nome do arquivo onde será salvo o csv
    
    columns : list, optional
        Lista com os nomes das colunas desejadas, se não especificado, todas as colunas serão lidas.
    
    Returns
    -------
    None
        Esta função baixa o CSV para o seu diretório local.
    '''
    try:
        # Chama a função que faz uma solicitação HTTP na URL e retorna o CSV em formato de texto
        textcsv = make_http_request(url)

        # Verifica se o texto CSV foi obtido com sucesso
        if textcsv is not None:
            # Cria um DataFrame com o CSV em formato de texto
            df = process_data(textcsv, columns)
            
            if df is not None:
                if local_file is not None:
                    # Salva o DataFrame no diretório local como a string passada pra local_file
                    df.to_csv(local_file, index=False)
                    print("CSV baixado e salvo localmente com sucesso.")
                else:
                    # Salva o DataFrame no diretório local como dados.csv
                    df.to_csv("dados.csv", index=False)
                    print("CSV baixado e salvo localmente com sucesso com nome default.")
            else:
                print("Falha ao processar os dados CSV, após ter feito o acesso à url.")
        else:
            print("Falha ao obter o CSV da URL.")
    except Exception as e:
        print("Ocorreu um erro durante o processo:", str(e))

if __name__ == "__main__":
    #Url do repositório usado para o trabalho
    url_repositorio = 'https://dadosabertos.eb.mil.br/arquivos/sermil/sermil2022.csv'

    download_csv_local(url_repositorio)