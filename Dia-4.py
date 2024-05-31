import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.neighbors import NearestNeighbors
from random import randint

import os
for dirname, _, filenames in os.walk('C:/Users/patri/OneDrive/Documentos/Códigos/Python/7-days-of-code-CD/Data/ml-100k'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current ses

data_filmes = pd.read_csv('C:/Users/patri/OneDrive/Documentos/Códigos/Python/7-days-of-code-CD/Data/ml-100k/u.item', sep='|', encoding='latin-1', header=None)
data_filmes.head()

data_notas = pd.read_csv('C:/Users/patri/OneDrive/Documentos/Códigos/Python/7-days-of-code-CD/Data/ml-100k/u.data', sep='\t', header = None)
data_notas.head()

#Renomeando e filtrando as colunas

data_notas.rename(columns={0 :'user_id', 1:'movie_id', 2:'rating', 3:'timestamp'}, inplace=True)
data_notas = data_notas[['user_id', 'movie_id', 'rating']]
data_notas

#Renomeando e filtrando as colunas da base de filmes.

data_filmes.rename(columns={0: 'movie_id', 1: 'movie_title', 2: 'release_date', 3: 'video_release_date', 4: 'imdb_url', 5:
'unknown', 6: 'action', 7: 'adventure', 8: 'animation', 9: 'childrens', 10: 'comedy', 11: 'crime', 12:
'documentary', 13: 'drama', 14: 'fantasy', 15: 'film_noir', 16: 'horror', 17: 'musical', 18: 'mystery', 19:
'romance', 20: 'scifi', 21: 'thriller', 22: 'war', 23: 'western'}, inplace=True)
data_filmes = data_filmes[['movie_id','movie_title']]
data_filmes

# Juntando as tabelas. Agora mostra o usuário, o que ele viu e qual a nota ele deu

df_ttd = pd.merge(data_notas, data_filmes, on='movie_id', how='left')
df_ttd = df_ttd[['user_id', 'movie_id', 'movie_title', 'rating']]
df_ttd

# Tramsformando no tipo json para poder subir no firebase

df_ttd.to_json('filmes_notas.json')

# Subindo minhas notas para os filmes

contador = 0
nome = input('Digite seu nome: ')
while contador < 5:
    sorteio = randint(0, len(data_filmes) - 1)
    dica = data_filmes['movie_title'][sorteio]
    nota = int(input(f"Nota para {dica}"))
    if nota > 0 :
        contador += 1
        usuario_nome = {'user_id': nome, 'movie_title' : dica, 'rating' : nota}
        df_ttd = pd.concat([df_ttd, pd.DataFrame([usuario_nome])], ignore_index=True)
print('FIM')

# Pivot deixa em um formato que produz a intersecção do usuário e  filme, mostrando a nota

# Fillna preenche valores nulos. Importante na hora da fórmula

#não é possível usar apenas o pivot porque o indice é duplicado


recomendacao = df_ttd.pivot_table(index='user_id', columns='movie_title', values='rating').fillna(0)

# Criando o modelo e alimentando com as informações

modelo = NearestNeighbors(metric='cosine')
modelo.fit(recomendacao)

# Executando o modelo de recomendação e dividindo em distância (indíce de proximidade) e vizinhos (os que são próximos )

distancia, vizinhos = modelo.kneighbors(recomendacao.loc[nome].values.reshape(1,-1), n_neighbors=6)

vizinhos

distancia

# Mostrando os usuários parecidos e suas distâncias

for i in range(0, len(distancia.flatten())):
    if i == 0:
        print(f'Usuário: {nome}\n')
    else:
        print(f'Vizinho: {recomendacao.index[vizinhos.flatten()[i]]} \nDistância de: {distancia.flatten()[i]}')
        
        # Dataset do usuário com suas notas

ds_usuario = recomendacao.loc[nome].to_frame()
ds_usuario

# Dataset do vizinho mais próximo com suas notas

vizinho_prox = recomendacao.index[vizinhos.flatten()[1]]
ds_vizinho = recomendacao.loc[vizinho_prox].to_frame()
ds_vizinho

# Junção dos datasets e mostrando ordem decrescente

ds_recomendacao = pd.merge(ds_usuario, ds_vizinho, on='movie_title').sort_values(by=vizinho_prox, ascending=False)

# Filtrando com os que o usuário que receberá a informação não tenha visto

ds_recomendacao = ds_recomendacao.query(f'{nome} == 0 and {recomendacao.index[vizinhos.flatten()[i]]} > 0')

ds_recomendacao[:5]

# Dataset do usuário

ds_usuario = recomendacao.loc[nome].to_frame()
ds_usuario

# Criando um novo dataset com o nome do filme e a nota dada pelo usuário, sem o indíce 
vizinhanca = ds_usuario
vizinhanca_df = vizinhanca.reset_index()
vizinhanca_df

# Acrescentando os vizinhos ao dataset 

for i in range(1, 6):
    vizinho_prox = recomendacao.index[vizinhos.flatten()[i]]
    ds_vizinho = recomendacao.loc[vizinho_prox].to_frame()
    vizinhanca = pd.merge(vizinhanca, ds_vizinho[vizinho_prox], on='movie_title')
    
#Resetando o index

vizinhanca = vizinhanca.reset_index()

# estabelecendo os vizinhos

pos1 = recomendacao.index[vizinhos.flatten()[1]]
pos2 = recomendacao.index[vizinhos.flatten()[2]]
pos3 = recomendacao.index[vizinhos.flatten()[3]]
pos4 = recomendacao.index[vizinhos.flatten()[4]]
pos5 = recomendacao.index[vizinhos.flatten()[5]]

# Acrescento os vizinhos e as notas dadas por eles. No final, faço uma coluna soma e indico os filmes favoritos do grupo

vizinhanca['SOMA'] = vizinhanca[pos1] + vizinhanca[pos2] + vizinhanca[pos3] + vizinhanca[pos4] + vizinhanca[pos5]
indicacao = vizinhanca.sort_values(by='SOMA', ascending=False)
indicacao = indicacao.query(f'{nome} == 0')
list(indicacao['movie_title'][:5])

indicacao

#exportando o modelo 

import pickle
filename = 'modelo_ptr.pk1'
pickle.dump(modelo, open(filename, 'wb'))
