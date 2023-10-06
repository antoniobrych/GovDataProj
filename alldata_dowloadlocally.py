from downloaddata import download_csv_local
import os

try:
    for i in range(2007,2023):
        if os.path.exists(f'sermil{i}.csv'):
            raise Exception

except:
    print("Os dados já estão baixados devidamente no seu local de trabalho.")
    pass

else:
    for i in range(2007,2023):        
            url_repositorio = f'https://dadosabertos.eb.mil.br/arquivos/sermil/sermil{i}.csv'
            download_csv_local(url_repositorio,local_file=f'sermil{i}.csv',dropna=True,columns=['PESO','ALTURA','DISPENSA'])