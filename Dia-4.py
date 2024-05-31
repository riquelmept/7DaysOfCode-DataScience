import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import os
for dirname, _, filenames in os.walk('C:/Users/patri/OneDrive/Documentos/Códigos/Python/7-days-of-code-CD/Data/ml-100k'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current ses

data_filmes = pd.read_csv('C:/Users/patri/OneDrive/Documentos/Códigos/Python/7-days-of-code-CD/Data/ml-100k/u.item', sep='|', encoding='latin-1', header=None, index_col=False)
data_filmes.head()

data_filmes.columns = ['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL', 'unknown',
                 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 
                 'Drama', 'Fantasy', 'FilmNoir', 'Horror', 'Musical', 'Mystery', 'Romance', 'SciFi', 
                 'Thriller', 'War', 'Western']
data_filmes.head

data_filmes.shape

data_filmes.info

data_filmes.video_release_date.unique()

data_filmes.drop(columns= ['video_release_date'], inplace = True)
data_filmes.head()

notas = pd.read_csv('C:/Users/patri/OneDrive/Documentos/Códigos/Python/7-days-of-code-CD/Data/ml-100k/u.data', encoding = 'latin-1', sep = "\t", header = None, index_col = False)
notas.columns = ['user_id', 'item_id', 'rating', 'timestamp']
notas.head()

notas.shape

notas.info()

notas.describe()
# Escolhendo o ID dos filmes como index
data_filmes = data_filmes.set_index('movie_id')

# Selecionando um filme através do seu ID (escolhendo pelo horário que estou digitando esta linha)
data_filmes.loc[1143]

totally_of_votes = notas['item_id'].value_counts()
totally_of_votes.head()

data_filmes['Total_de_Votos'] = totally_of_votes
data_filmes.head()

data_filmes.sort_values('Total_de_Votos', ascending = False)

notas_medias = notas.groupby("item_id").mean()['rating']
notas_medias.head()

data_filmes['Nota_Media'] = notas_medias
data_filmes.head()

data_filmes.sort_values("Nota_Media", ascending= False).head(15)

data_filmes.query('Total_de_Votos >= 10').sort_values('Nota_Media', ascending= False)

data_filmes.Total_de_Votos.min()

data_filmes.Total_de_Votos.max()

filmes_com_mais_de_100_votos = data_filmes.query('Total_de_Votos >= 50')
filmes_com_mais_de_100_votos.sort_values('Nota_Media', ascending = False)

filmes_com_mais_de_100_votos.sample(10)

assistido = [20, 186, 303, 168, 255, 658, 636, 825, 82, 491]
filmes_com_mais_de_100_votos.query('Action == 1 and Drama == 1')

acao_drama = filmes_com_mais_de_100_votos.query('Action == 1 and Drama == 1')
acao_drama.sort_values('Nota_Media', ascending = False).head(5)

# Deste resultado, eu exclui os filmes que já assisti:
acao_drama.drop(assistido, errors = 'ignore').sort_values('Nota_Media', ascending = False).head(5)

usuario_50 = notas.query('user_id == 50')
usuario_50[['item_id', 'rating']].set_index('item_id')

def historico_usuario(usuario):
    historico_usuario = notas.query('user_id == %d' % usuario)
    historico_usuario = historico_usuario[['item_id', 'rating']].set_index('item_id')
    return historico_usuario

historico_usuario(50)

historico_usuario(75)

user50 = historico_usuario(43)
user75 = historico_usuario(62)

user50.join(user75, lsuffix='_do_user', rsuffix='_comparacao').dropna()

diferenca = user50.join(user75, lsuffix='_do_user',rsuffix='_comparacao').dropna()
np.linalg.norm(diferenca['rating_do_user'] - diferenca['rating_comparacao'])

def distancia_entre_perfis(user_id1, user_id2):
    notas1 = historico_usuario(user_id1)
    notas2 = historico_usuario(user_id2)
    diferenca = notas1.join(notas2, lsuffix = '_do_user', rsuffix = '_comparacao').dropna()
    distancia = np.linalg.norm(diferenca['rating_do_user'] - diferenca['rating_comparacao'])
    return [user_id1, user_id2, distancia]

distancia_entre_perfis(50, 75)

notas.user_id.unique()

print('O dataset possui %d usuarios.' % len(notas.user_id.unique()))

usuario1 = 50

distancias = []
for usuario in notas['user_id'].unique():
    calculo = distancia_entre_perfis(usuario1, usuario)
    distancias.append(calculo)

distancias[:5]

# Função para calcular a distância entre 1 usuário específico e os demais:

def distancia_entre_usuarios(usuario_1):
    todos_os_usuarios = notas['user_id'].unique()
    distancias = [distancia_entre_perfis(usuario_1, user_id) for user_id in todos_os_usuarios]
    distancias = pd.DataFrame(distancias, columns = ['Usuario_1', 'Outro_user', 'Distancia'])
    return distancias

distancia_entre_usuarios(50).head()

# Ordenando o Dataframe pela Distância:

def mais_proximos_de(usuario_1):
    distancias = distancia_entre_usuarios(usuario_1)
    distancias = distancias.sort_values('Distancia')
    distancias = distancias.set_index('Outro_user').drop(usuario_1)
    return distancias

mais_proximos_de(50)

mais_proximos_de(50).head(20)

def distancia_entre_perfis(user_id1, user_id2, minimo = 5):
    notas1 = historico_usuario(user_id1)
    notas2 = historico_usuario(user_id2)
    diferenca = notas1.join(notas2, lsuffix = '_do_user', rsuffix = '_comparacao').dropna()
    
    if(len(diferenca) < minimo):
        return None
    
    distancia = np.linalg.norm(diferenca['rating_do_user'] - diferenca['rating_comparacao'])
    return [user_id1, user_id2, distancia]

def distancia_entre_usuarios(user_1, numero_maximo_de_analise = None):
    todos_os_usuarios = notas['user_id'].unique()
    
    if numero_maximo_de_analise:
        todos_os_usuarios = todos_os_usuarios[:numero_maximo_de_analise]
        
    distancias = [distancia_entre_perfis(user_1, user_id) for user_id in todos_os_usuarios]
    distancias = list(filter(None, distancias))
    distancias = pd.DataFrame(distancias, columns = ['Usuario_1', 'Outro_user', 'Distancia'])
    return distancias

def mais_proximos_de(user_1, quantidade_user_proximos = 10, numero_maximo_de_analise = None):
    distancias = distancia_entre_usuarios(user_1, numero_maximo_de_analise = numero_maximo_de_analise)
    distancias = distancias.sort_values('Distancia')
    distancias = distancias.set_index('Outro_user').drop(user_1)
    return distancias.head(quantidade_user_proximos)

mais_proximos_de(196, numero_maximo_de_analise = 50)

def sugestoes(user1, quantidade_user_proximos = 10, numero_maximo_de_analise = None):
    notas_user1 = historico_usuario(user1)
    historico_filmes = notas_user1.index
    similares = mais_proximos_de(user1, quantidade_user_proximos = quantidade_user_proximos, 
                                 numero_maximo_de_analise = numero_maximo_de_analise)
    usuarios_similares = similares.index
    notas_dos_similares = notas.set_index('user_id').loc[usuarios_similares]
    recomendacoes = notas_dos_similares.groupby('item_id').mean()[['rating']]
    recomendacoes = recomendacoes.sort_values('rating', ascending = False)
    return recomendacoes.join(data_filmes).head()

sugestoes(196, quantidade_user_proximos = 2, numero_maximo_de_analise = 50)

sugestoes(196, numero_maximo_de_analise = 50)

sugestoes(196)

data_filmes.sample(11)

import random
notas_novo_user = [random.randint(1,5) for x in range(11)]
notas_novo_user

def novo_usuario(seus_filmes):
    novo_usuario = notas['user_id'].max()+1
    notas_do_usuario_novo = pd.DataFrame(seus_filmes, columns = ['item_id', 'rating'])
    notas_do_usuario_novo['user_id'] = novo_usuario
    return pd.concat([notas, notas_do_usuario_novo])

notas = novo_usuario([[723, 3], [1094, 3], [652, 1], [1522, 5], [1243, 2], [1456, 1], [1086, 5], [1034, 2], [703, 2], [90, 3], [217, 2]])
notas.tail(12)

# Para o novo usuário temos as seguintes recomendações:

sugestoes(944)