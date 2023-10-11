# Funções para preparar o dataframa pra visualização

def take_data(csv_file, columns):
    import pandas as pd
    """
    Parameters
    ----------
    csv_file : str
        Nome do arquivo CSV que queremos transformar em um DataFrame.
    columns : list
        Lista com os nomes das colunas que desejamos extrair do arquivo CSV.

    Returns
    -------
    novo_df : pandas.core.frame.DataFrame
        Retorna um DataFrame contendo apenas as colunas desejadas do arquivo CSV.
        
    Raises
    ------
    FileNotFoundError
        Se o arquivo CSV não for encontrado.
    ValueError
        Se nenhuma das colunas especificadas existir no arquivo CSV.

    Examples
    --------
    Exemplo 1: Extrair uma única coluna do arquivo CSV.
    
    # Criando dado para exemplo
    >>> data = {'Nome': ['Alice', 'Bob', 'Charlie'],
    ...         'Idade': [25, 30, 35],
    ...         'Cidade': ['São Paulo', 'Rio de Janeiro', 'Brasília']}
    >>> df = pd.DataFrame(data)
    
    # Criando um arquivo CSV temporário com os dados
    >>> csv_file = 'exemplo.csv'
    >>> df.to_csv(csv_file, index=False)
    
    # Extraiindo a coluna 'Nome' do arquivo
    >>> resultado = take_data(csv_file, ['Nome'])
    >>> print(resultado)
          Nome
    0    Alice
    1      Bob
    2  Charlie

    """
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')

        # Verifica se as colunas especificadas existem no DataFrame
        colunas_existentes = [col for col in columns if col in df.columns]

        if not colunas_existentes:
            raise ValueError("Nenhuma das colunas especificadas existe no arquivo CSV.")

        # Cria um novo DataFrame apenas com as colunas desejadas
        novo_df = df[colunas_existentes]

        return novo_df

    except FileNotFoundError as e:
        raise FileNotFoundError(f"O arquivo CSV '{csv_file}' não foi encontrado.") from e

    except Exception as e:
        raise Exception(f"Ocorreu um erro ao ler o arquivo CSV: {str(e)}") from e

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)



def transform_column(df, coluna, transform_dict):
    import pandas as pd
    """
    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        Recebe um dataframe que terá colunas transformadas.
    coluna : str
        Recebe o nome da coluna que queremos transformar.
    transform_dict : dict
        Recebe um dicionário com as chaves sendo itens a serem tranformados, e 
        os valores sendo a transformação.

    Returns
    -------
    df : pandas.core.frame.DataFrame
        retorna o data frame com as colunas transformadas.
    
    Examples
    --------
    # Exemplo 1: Transformar a coluna 'ESCOLARIDADE' de acordo com um dicionário
    >>> import pandas as pd
    >>> data = {'ESCOLARIDADE': ['Ensino Fundamental', 'Ensino Médio',
    ...                          'Ensino Superior', 'Mestrado']}
    >>> df = pd.DataFrame(data)
    >>> transform_dict = {'Ensino Fundamental': 'Fundamental',
    ...                   'Ensino Médio': 'Médio', 'Ensino Superior': 'Superior'}
    >>> resultado = transform_column(df, 'ESCOLARIDADE', transform_dict)
    >>> list(resultado['ESCOLARIDADE'])  
    ['Fundamental', 'Médio', 'Superior', 'Mestrado']

    # Exemplo 2: Tentar transformar uma coluna que não existe no DataFrame
    >>> df = pd.read_csv("sermil2022.csv")
    >>> transform_column(df,"importante",{"importante":"urgente"})
    A coluna 'importante' não existe no DataFrame.
    
    # Exemplo 3: Transformar uma coluna vazia com um dicionário vazio
    >>> df = pd.DataFrame({'NOME': []})
    >>> transform_dict = {}
    >>> resultado = transform_column(df, 'NOME', transform_dict)
    >>> list(resultado['NOME'])  
    []
    
    """

    if coluna not in df.columns:
        print(f"A coluna '{coluna}' não existe no DataFrame.")
        return None

    for original, transformado in transform_dict.items():
        df[coluna] = df[coluna].str.replace('.*' + original + '.*', transformado, regex=True)

    return df

