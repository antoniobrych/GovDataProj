"""
Rascunho:
Gráfico de barras com o nível de escolaridade dos alistados
"""
import pandas as pd

def take_data(csv_file, columns):
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

"""
#transformar isso em func
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Fundamental' if 'Ensino Fundamental' in x else x)
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Médio' if 'Ensino Médio' in x else x)
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Superior' if 'Ensino Superior' in x else x)
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Superior' if 'Mestrado' in x else x)
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Superior' if 'Doutorado' in x else x)
novo_df['ESCOLARIDADE'] = novo_df['ESCOLARIDADE'].apply(lambda x: 'Ensino Superior' if 'Pós-Graduaç' in x else x)

#transformar em func pra gerar grafico
contagem_escolaridade = novo_df['ESCOLARIDADE'].value_counts()
plt.figure(figsize=(10, 6))  
contagem_escolaridade.plot(kind='bar')
plt.title('Distribuição de Escolaridade')
plt.xlabel('Grau de Escolaridade')
plt.ylabel('Número de Pessoas')

plt.show()
"""