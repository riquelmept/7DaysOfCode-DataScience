#Importando biblioteca pandas

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as pyof
import plotly.graph_objs as pygo

despesa_2022 = pd.read_csv('C:/Users/patri/OneDrive/Documentos/Códigos/Python/7-days-of-code-CD/Data/despesa_ceaps_2022.csv', encoding='ISO-8859-1',delimiter=';', skiprows= 1)

despesa_ttd = despesa_2022
despesa_ttd = despesa_ttd.drop(1)

despesa_ttd.columns
despesa_ttd.info()

despesa_ttd['DETALHAMENTO'].fillna('Não informado', inplace=True)

despesa_ttd['DOCUMENTO'].fillna('Não informado', inplace=True)

despesa_ttd.info()

pd.to_datetime(despesa_ttd['DATA'].str.title(), format='%d/%m/%Y')

despesa_ttd['DATA'] = pd.to_datetime(despesa_ttd['DATA'].str.title(), format='%d/%m/%Y')
despesa_ttd

despesa_ttd['VALOR_REEMBOLSADO'].str.replace(',','.').astype(float)

despesa_ttd['VALOR_REEMBOLSADO'] = despesa_ttd['VALOR_REEMBOLSADO'].str.replace(',','.').astype(float)
despesa_ttd

duplicados = despesa_ttd.duplicated()
duplicados.sum()

despesa_ttd.info()

despesa_ttd.to_csv('despesa_ttd.csv', sep = ',', index = False)

sum(despesa_ttd['DATA'] <= '2021-09-30')

previous_2021 = (despesa_ttd['DATA'] <= '2021-09-30')
despesa_ttd[previous_2021]

data_irregular = despesa_ttd[previous_2021]

despesa_ttd.drop(labels = data_irregular.index, inplace = True)
despesa_ttd

despesa_ttd.TIPO_DESPESA.value_counts()

trace = pygo.Scatter(x = despesa_ttd['TIPO_DESPESA'],
                   y = despesa_ttd['VALOR_REEMBOLSADO'],
                   mode = 'markers')
data = [trace]
pyof.iplot(data)

#Análise visual da distribuição das despesas

plt.figure(figsize=(15, 8))
ax = sns.histplot(data = despesa_ttd, x = "TIPO_DESPESA", y='VALOR_REEMBOLSADO');
ax.set_title("Despesas")
plt.xlabel('Tipo de despesa')
plt.ylabel('Valor do reembolso')
plt.title('Distribuição das despesas', fontsize=20)
ax.tick_params(axis='x', rotation=90)
plt.show()

despesa_ttd.SENADOR.value_counts()

despesa_ttd.groupby(['SENADOR'])['VALOR_REEMBOLSADO'].agg('sum').round(2)

trace = pygo.Scatter(x = despesa_ttd['SENADOR'],
                   y = despesa_ttd['VALOR_REEMBOLSADO'],
                   mode = 'markers')
data = [trace]
pyof.iplot(data)

maiores_pedintes_reembolso = despesa_ttd.groupby(['SENADOR'])['VALOR_REEMBOLSADO'].agg('sum').round(2)

maiores_pedintes_reembolso.sort_values(ascending=False).head(10).plot(kind='bar', 
                                                         title='Senadores com maiores valores de reembolso',
                                                         figsize=(15, 8));

despesa_ttd.DATA.value_counts()

despesa_ttd.groupby(['DATA'])['VALOR_REEMBOLSADO'].agg('sum').round(2)

trace = pygo.Scatter(x = despesa_ttd['DATA'],
                   y = despesa_ttd['VALOR_REEMBOLSADO'],
                   mode = 'markers')
data = [trace]
pyof.iplot(data)

despesa_ttd.MES.value_counts()

despesa_ttd.groupby(['MES'])['VALOR_REEMBOLSADO'].agg('sum').round(2)

trace = pygo.Bar(x = despesa_ttd['MES'],
                   y = despesa_ttd['VALOR_REEMBOLSADO'])
data = [trace]
pyof.iplot(data)