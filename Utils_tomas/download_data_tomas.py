import requests
import importlib
from typing import List

def check_libraries() -> List[str]:
    '''
    Verifica se as bibliotecas necessárias estão instaladas.

    Returns
    -------
    List[str] or None
        Retorna uma lista de bibliotecas ausentes ou None se todas as bibliotecas estiverem instaladas.

    Example
    -------
    >>> missing_libs = check_libraries()
    >>> isinstance(missing_libs, list) or missing_libs is None
    True
    '''

    missing_libraries = []
    req_lib = [
        'unittest',
        'io',
        'requests',
        'doctest',
        'pandas',
        'numpy',
        'datetime',
        'typing',
        'geopandas',
        'matplotlib',
        'seaborn',
        'os'
    ]
    for lib in req_lib:
        try:
            importlib.import_module(lib)
        except ImportError:
            missing_libraries.append(lib)
    if missing_libraries:
        return missing_libraries
    else:
        return None

def download_gpkg_local(url: str) -> bool:
    '''
    Faz o download do um arquivo dado uma url

    Parameters
    ----------
    url: str
        A URL do arquivo que será baixado.

    Returns
    -------
    bool
        Retorna True ou False que indica se o download do arquivo foi efetuado com sucesso.

    Example
    -------
    >>> result = download_gpkg_local("https://ESSA_URL_N_EXISTE.com")
    >>> result is None
    True
    '''
    try:
        data_gpkg = requests.get(url)
        if data_gpkg.status_code == 200:
            with open("geo_data.gpkg", 'wb') as file:
                file.write(data_gpkg.content)
            return True
    except:
        return None
