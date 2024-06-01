# Packages imports
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.stats.api as sms
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from math import ceil

# o effect size é a mudança desejada. 
# nesse caso, está dizendo que tem uma taxa de treze porcento e quer chegar até 15 porcento de sucesso

effect_size = sms.proportion_effectsize(0.13, 0.15)     

# Aqui está dizendo qual o minímo de amostras que é necessário. 
# O power = 0.8 é uma conveção, o alpha como 0,05 significa que qualquer ateração menor que isso não vale a pena considerar


required_n = sms.NormalIndPower().solve_power(
    effect_size, 
    power=0.8, 
    alpha=0.05, 
    ratio=1
    )                                                  

# Arredonda pra cima
required_n = ceil(required_n)                                                  

print(required_n)

# Subi os arquivos e mostrei o topo

df_teste = pd.read_csv('C:/Users/patri/OneDrive/Documentos/Códigos/Python/7-days-of-code-CD/Data/ab_data.csv')

df_teste.head()

df_teste.info()

# cruzando as tabelas e verificando onde os dados se cruzam, parecido com pivotar

pd.crosstab(df_teste['group'], df_teste['landing_page'])

#verificando se usuários aparecem mais do que uma vez

session_counts = df_teste['user_id'].value_counts(ascending=False)
multi_users = session_counts[session_counts > 1].count()

print(f'Há {multi_users} usuários que aparecem múltiplas vezes no dataset')

# Apagou os usuários que se repetem


users_to_drop = session_counts[session_counts > 1].index

df_teste = df_teste[~df_teste['user_id'].isin(users_to_drop)]
print(f'O dataset foi atualizado e agora tem {df_teste.shape[0]} entradas')

# Criando o grupo controle e o experimental de maneira randômica

control_sample = df_teste[df_teste['group'] == 'control'].sample(n=required_n, random_state=23)
treatment_sample = df_teste[df_teste['group'] == 'treatment'].sample(n=required_n, random_state=23)

# juntando as amostras
ab_test = pd.concat([control_sample, treatment_sample], axis=0)
ab_test.reset_index(drop=True, inplace=True)

ab_test

ab_test.info()

ab_test['group'].value_counts()

# Vendo a taxa de conversão por grupo

conversion_rates = ab_test.groupby('group')['converted']

# Criando uma função para o desvio padrão
std_p = lambda x: np.std(x, ddof=0)              

#  Criando outra função para calcular o erro do desvio 
se_p = lambda x: stats.sem(x, ddof=0)            

# O agg aplica as funções na lista no dataframe 
conversion_rates = conversion_rates.agg([np.mean, std_p, se_p])
conversion_rates.columns = ['conversion_rate', 'std_deviation', 'std_error']


conversion_rates.style.format('{:.3f}')

# Plotando os gráficos  e mostrando que a taxa não mudou muito

plt.figure(figsize=(8,6))

sns.barplot(x=ab_test['group'], y=ab_test['converted'], ci=False)

plt.ylim(0, 0.17)
plt.title('Conversion rate by group', pad=20)
plt.xlabel('Group', labelpad=15)
plt.ylabel('Converted (proportion)', labelpad=15);

from statsmodels.stats.proportion import proportions_ztest, proportion_confint

control_results = ab_test[ab_test['group'] == 'control']['converted']
treatment_results = ab_test[ab_test['group'] == 'treatment']['converted']

n_con = control_results.count()
n_treat = treatment_results.count()

# successes: todos os convertidos em uma lista
successes = [control_results.sum(), treatment_results.sum()]

# Todos os casos em uma lista
nobs = [n_con, n_treat]

# Separando os sucessos dos casos totais
z_stat, pval = proportions_ztest(successes, nobs=nobs)
(lower_con, lower_treat), (upper_con, upper_treat) = proportion_confint(successes, nobs=nobs, alpha=0.05)

print(f'z statistic: {z_stat:.2f}')
print(f'p-value: {pval:.3f}')
print(f'ci 95% for control group: [{lower_con:.3f}, {upper_con:.3f}]')
print(f'ci 95% for treatment group: [{lower_treat:.3f}, {upper_treat:.3f}]')

successes = [control_results.sum(), treatment_results.sum()]