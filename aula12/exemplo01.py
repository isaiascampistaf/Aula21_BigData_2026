import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt


# Obtendo os dados
try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    # utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencias)

    #df_ocorrencias = df_ocorrencias[df_ocorrencias['regiao'] == 'Baixada Fluminense']##########


    # delimitando os dados
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    # print(df_roubo_veiculo.head(30))
    # print(df_roubo_veiculo.tail(30))


    # ### PREPARANDO OS DADOS
    # Totalizando os roubos por cidade (Var Qualitativa 'munic' e Var Quant 'roubo_veiculo')
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()


    # Ordenando os dados
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo',
        ascending=False
    )

    print(df_roubo_veiculo.head(10))
    # print(df_roubo_veiculo.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')



try:
    print(f'\nObtendo informações a cerca dos roubos dos veículos...')
    array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia = abs(
        (media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100
    )

    print('\nMedidas de Tendência Central')
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância Média - Mediana: {distancia:.2f}%')


except Exception as e:
    print(f'Obtendo Medidas - {e}')



# Calculando os quartis
try:
    print(f'\nSeparando os quartis...')
    q1 = np.quantile(array_roubo_veiculo, .25)
    q2 = np.quantile(array_roubo_veiculo, .50)
    q3 = np.quantile(array_roubo_veiculo, .75)

    print('\nMedidas de Posição')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')

    # Cidades c/ menos ocorrências de roubos
    df_roubo_veiculo_menores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] < q1
    ]

    # Cidades c/ maiores ocorrências de roubos
    df_roubo_veiculo_maiores = df_roubo_veiculo[
        df_roubo_veiculo['roubo_veiculo'] > q3
    ]

    # Menores
    print('\nMunicípios com menores roubos')
    print(30*'-')
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    # Exportando o dataframe
    # index=False - Não exporta os índices. Salva os dados das colunas munic e roubo_veiculo
    # sep=';' - Altera o separador de colunas para ';'
    # encoding='iso-8859-1' - Informa o encoding para salvar o csv. "Pode ser o mesmo"
    # df_roubo_veiculo_menores.to_csv('menores.csv', index=False, sep=';', encoding='iso-8859-1')

    # Maiores
    print('\nMunicípios com maiores roubos')
    print(30*'-')
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))
    # Exportando o dataframe
    # df_roubo_veiculo_maiores.to_csv('maiores.csv', index=False, sep=';', encoding='iso-8859-1')


except Exception as e:
    print(f'Erro ao analizar a distribuição {e}')


# Medidas de Posição e Dispersão
try:
    print('\nCalculando a Amplitude Total')
    
    # anplitude_total = maior - menor
    # Quanto mais próximo do 0, mais homogêneos são os dados do conjunto.
    # Quanto mais próximo do maior valor, mais heterogêneos são os dados do conjunto.
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude = maximo - minimo

except Exception as e:
    print(f'Erro ao calcular a amplitude: {e}')

# Medidas de Dispersão
try: 
    #Variancia
    #É uma medida p/observar a dispersão dos dados.
    #Observa se em relação a média.
    #É a media dos quadrados das diferenças entre cada valor e a media
    #OBS: O resultado da Variancia esta elevado ao Quadrado 
    variancia = mp.var(array_roubo_veiculo)

    #distancia variancia media 
    # < 10% - Baixa Dispersão
    #Entre 10% e 25% - Tendência de Moderada Dispersão 
    #Acima de 25% Alta Dispersão 
    distancia_var_media = variancia / (media_roubo_veiculo ** 2) * 100 

    #Desvio Padrão 
    #É a raiz quadrada da Variancia. Obersava-se em relação a media. 
    #É a normalização da variancia.
    #Quanto os dados se afastam da Média. 
    desvio_padrao = np.std(array_roubo_veiculo)

    #Coeficiente de variação
    # É a magnitude do desvio padrao em relacao a media 
    coef_variacao = (desvio_padrao / media_roubo_veiculo) * 100

except Exception as e:
    print(f'Erro ao calcular a variabilidade do conjunto: {e}')

# Achando os outliers
try:
    # Intervalo Interquartil (IQR)
    # É a amplitude dos dados mais centrais
    # Ignora o maior e o menor valor
    # Não sofre interferência dos Extremos
    # Quanto mais próximo do 0, mais homogêneos são os dados mais centrais
    # Quanto mais próximo do Q3, mais heterogêneos são os dados dos 50% mais centrais
    # 970.75
    iqr = q3 - q1

    # calculando os limites
    # Superior
    limite_superior = q3 + (1.5 * iqr)

    # Inferior
    limite_inferior = q1 - (1.5 * iqr)


    print(f'\nLimite Superior: {limite_superior}')
    print(f'\nLimite Inferior: {limite_inferior}')

    # Filtrando os outliers menores
    df_roubo_veiculo_outliers_menores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] < limite_inferior]
    )

    # Printando os outliers menores
    print('\nMunicípios com outliers inferiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_menores) == 0:
        print('Não há outliers Inferiores')
    else:
        print(df_roubo_veiculo_outliers_menores)
    

    # Printando os outliers maiores
    df_roubo_veiculo_outliers_maiores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo'] > limite_superior]
    )

    print('\nMunicípios com outliers superiores')
    print(30*'-')
    if len(df_roubo_veiculo_outliers_maiores) == 0:
        print('Não há outliers Superiores')
    else:
        print(df_roubo_veiculo_outliers_maiores)

except Exception as e:
    print(f'Erro ao calcular os outliers {e}')


try:
    print('\nMostrando Medidas')
    print(30*'-')
    print(f'Mínimo: {minimo}')
    print(f'Limite Inferior: {limite_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'Limite Superior: {limite_superior}')
    print(f'Máximo: {maximo}')

    print(f'\nMédia: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância: {distancia}')
    print(f'IQR: {iqr}')
    print(f'Amplitude: {amplitude}')    
    
    print(f'Variãncia: {variancia:.2f}')    
    print(f'Distancia Variancia e Media: {distancia_var_media:.2f}')
    print(f'Desvio Padrão: {desvio_padrao:2f}')
    print(f'Coeficiente de Variação: {coef_variacao:2f}')


except Exception as e:
    print(f'\nErro ao mostrar medidas {e}')


# # Plotando Gráfico
# try:
#     print('Plotando BoxPlot')
#     # pip install matplotlib 
#     # import matplotlib.pyplot as plt

#     # BoxPlot
#     # Retirar os outliers - showfliers=False  
#     # Coloar a média - showmeans=True
#     plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation='horizontal', showmeans=True)
#     plt.show()

# except Exception as e:
#     print(f'Erro ao plotar o grafico: {e}')


try:
    print('\nInformações de Roubos de Veículos')
    plt.figure(figsize=(16, 10))


    # Posição 01 - Boxplot
    plt.subplot(2, 2, 1)

    #showmeans - mostra a média, showfliers = remove os outliers 
    plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation='horizontal', showmeans=True, showfliers=True) 
    plt.title('Distribuição dos dados')
    plt.xlabel('Roubo de Veículos')
    # plt.ylabel('Municípios')


    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.95, f'Limite Inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.90, f'Mínimo: {minimo}', fontsize=12)
    plt.text(0.1, 0.85, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.80, f'Q2: {q2}', fontsize=12)
    plt.text(0.1, 0.75, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.70, f'Limite Superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.65, f'Máximo: {maximo}', fontsize=12)

    plt.text(0.1, 0.55, f'Mediana: {mediana_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.50, f'Média: {media_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.45, f'IQR Intervalo Interquartil: {iqr}', fontsize=12)
    plt.text(0.1, 0.40, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.text(0.1, 0.35, f'Distância: {distancia}', fontsize=12)
    
    plt.axis('off')
    
    # Barras -  | 10 Menores Valores
    plt.subplot(2,2,3)

    #Ordenar crescente ou decrescente aqui  asceding= true

    df_roubo_veiculo_10menores = (
        df_roubo_veiculo_menores.tail(10)
    )

    plt.barh(df_roubo_veiculo_10menores['munic'], df_roubo_veiculo_10menores['roubo_veiculo'])
    plt.title('Bottom 10 - Municipios com menores roubos')

    # 4ª Posição Colunas | Top 10 maiores
    plt.subplot(2,2,4)

    #Filtrando e Ordenando
    df_roubo_veiculo_10maiores = (
        df_roubo_veiculo_maiores
        .head(10)
        .sort_values(by='roubo_veiculo', ascending= True)
    )


    plt.bar(df_roubo_veiculo_10maiores['munic'],df_roubo_veiculo_10maiores['roubo_veiculo'])
    plt.xlabel('Municipios')
    plt.ylabel('Roubo de Veiculos')
    plt.xticks(rotation=45, ha='right')  #Rotaciona 

    plt.suptitle('Informações sobre Roubos de Veículos') 

    plt.show()

except Exception as e:
    print(f'Erro ao plotar o grafico: {e}')

    