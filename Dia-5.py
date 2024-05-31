# Importei as bibliotecas necessárias. 
# Flask cria a conexão e disponibiliza online
# pickle carrega o modelo de machine learning

import numpy as np
from flask import Flask
import pickle
import pandas as pd
import requests
import json

# carregando o modelo de machine learning

modelo = pickle.load(open('modelo_ptr.pk1','rb'))

# Perguntando para quem será recomendado

pos = int(input('Para quem recomendar: '))

# Criando a aplicação
app = Flask(__name__)

# endpoint mostrando que o site está funcionando
@app.route('/')
def mensagem():
    return "FUNCIONANDO"

# endpoint fazendo a indicação
@app.route('/indica')
def indica():
    # dados salvo na nuvem
    df = requests.get('https://recomendacao-95a6d-default-rtdb.firebaseio.com/.json')
    df = df.json()
    df = pd.DataFrame(df)
    recomendacao = df.pivot_table(index='user_id', columns='movie_title', values='rating').fillna(0)
    distancia, vizinhos = modelo.kneighbors(recomendacao.iloc[pos].values.reshape(1,-1), n_neighbors=6)
    ds_usuario = recomendacao.iloc[pos].to_frame()
    vizinhanca = ds_usuario
    for i in range(1, 6):
        vizinho_prox = recomendacao.index[vizinhos.flatten()[i]]
        ds_vizinho = recomendacao.loc[vizinho_prox].to_frame()
        vizinhanca = pd.merge(vizinhanca, ds_vizinho[vizinho_prox], on='movie_title')
    pos1 = recomendacao.index[vizinhos.flatten()[1]]
    pos2 = recomendacao.index[vizinhos.flatten()[2]]
    pos3 = recomendacao.index[vizinhos.flatten()[3]]
    pos4 = recomendacao.index[vizinhos.flatten()[4]]
    pos5 = recomendacao.index[vizinhos.flatten()[5]]
    vizinhanca_df = vizinhanca.reset_index()
    vizinhanca_df.rename(columns={pos + 1 : 'coluna'}, inplace=True)
    vizinhanca_df['SOMA'] = vizinhanca_df[pos1] + vizinhanca_df[pos2] + vizinhanca_df[pos3] + vizinhanca_df[pos4] + vizinhanca_df[pos5]
    indicacao = vizinhanca_df.sort_values(by='SOMA', ascending=False)
    indicacao.query('coluna == 0')
    resposta = str(list(indicacao['movie_title'][:5]))
    return resposta

if __name__ == "__main__":
    app.run()