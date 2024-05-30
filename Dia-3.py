#Importando biblioteca pandas

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as pyof
import plotly.graph_objs as pygo
from prophet import Prophet

dados_ceaps = pd.read_csv('C:/Users/patri/OneDrive/Documentos/Códigos/Python/7-days-of-code-CD/Data/dataset_ceaps_forecasting.csv', encoding='ANSI')
dados_ceaps

a = Prophet()
a.fit(dados_ceaps)

prox_3meses = a.make_future_dataframe(periods=90)
prox_3meses

previsao = a.predict(prox_3meses)
previsao[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

fig1 = a.plot(previsao)

fig2 = a.plot_components(previsao)

from prophet.plot import plot_plotly, plot_components_plotly

plot_plotly(a, previsao)