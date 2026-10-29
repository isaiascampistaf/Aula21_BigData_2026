import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 

try:   
   print('Obtendo os dados...') 

   ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

   df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

   df_cvli = df_ocorrencias[['aisp','cvli']]

   df_cvli = df_cvli.groupby('aisp', as_index=False)['cvli'].sum()
 

#    print(df_aisp) 



except Exception as e:
    print(f'Erro ao obter os dados - {e}')


try: 
    array_cvli = np.array(df_cvli['cvli'])

    media_cvli = np.mean(array_cvli)
    mediana_cvli = np.median(array_cvli)
    
    distancia1 = abs(
        (media_cvli - mediana_cvli) / mediana_cvli * 100 
    )
    print('\nMedidas de Tendência Central')
    print(f'Média: {media_cvli}')
    print(f'Mediana: {mediana_cvli}')
    print(f'Distância Média - Mediana: {distancia1:.2f}%')


except Exception as e: 
    print(f'Obtendo Medidas - {e}')

try:
    print(f'\nSeparando os quartis...')
    q1 = np.quantile(array_cvli, .25)
    q2 = np.quantile(array_cvli, .50)
    q3 = np.quantile(array_cvli, .75)

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # aisp c/ menos ocorrências de cvli
    df_cvli_menores = df_cvli[
        df_cvli['cvli'] < q1
    ]

    # aisp c/ maiores ocorrências de cvli
    df_cvli_maiores = df_cvli[
        df_cvli['cvli'] > q3
    ]

    print('\nMunicípios com menores roubos')
    print(30*'-')
    print(df_cvli_menores.sort_values(by='cvli', ascending=True))

    print('\nMunicípios com maiores roubos')
    print(30*'-')
    print(df_cvli_maiores.sort_values(by='cvli', ascending=False))



except Exception as e:
    print(f'Erro ao analizar a distribuição {e}')

try:
    print('\nCalculando a Amplitude Total')

    maximo = np.max(array_cvli)
    minimo = np.min(array_cvli)
    amplitude = maximo - minimo

    print(amplitude)

except Exception as e: 
    print(f'Erro ao calcular a amplitude: {e}')

    

