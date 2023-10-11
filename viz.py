    Parameters
    ----------
    url : str
        A URL que aponta para o conjunto de dados a ser lido.
    
    dropna : bool
        Argumento para tirar ou nao linhas com valores nulos.
    
    local_file : str, optional
        Nome do arquivo onde sera salvo o csv. Por padrão o nome sera
        'dados.csv'.
    
    columns : list, optional
        Lista com os nomes das colunas desejadas, se nao especificado, todas as colunas serao lidas.
    
    Returns
    -------
    None
        Esta funcao baixa o CSV para o seu diretorio local