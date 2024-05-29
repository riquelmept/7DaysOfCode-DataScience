#Importando biblioteca pandas

import pandas as pd

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