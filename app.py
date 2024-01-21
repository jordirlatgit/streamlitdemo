import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.write(""" 
# Hello World!
""")

#df = pd.read_csv('2023_10_Aire_BCN.csv')  #dades del mes d'octubre
csv_url= "https://github.com/jordirlatgit/streamlitdemo/blob/main/2023_11_Aire_BCN.csv"
df = pd.read_csv(csv_url)
#df_2 = pd.read_csv('2023_12_Aire_BCN.csv')

df.head()

# %%
df.info()

# %% [markdown]
# Identificador 0 al 3: Codi de la provincia, Provincia,Codi del municipi i municipi -- són valors únics. Per a totes les dades és Barcelona, per tant no serà necessari
# Identificador 4: Estació -- indica en quina de les estacions de mesura es va obtenir aquella dada  8 estacions
# Identificador 5: Codi Contaminant -- indica el tipus de contaminant 22 contaminants
# Identificador 6 i 7: L'any i el mes -- per aquest datasheet també és unic tots són 2023 i gener
# Identificador 8: El dia va referència als dies del mes
# Identificador 9: hora de la mesura
# Identificador 10: validació de la mesura
# 
# La resta de columnes són iguals per les 24h del dia
# 

# %%
df.isna().sum() #busquem possibles nulls

# %%
df_1=df[["DIA","ESTACIO","CODI_CONTAMINANT"]]
df_1

# %% [markdown]
# De les 2015 files detectem un màxim dade nules al valors HX referents a les hores.
# S'ha buscat si els valors nuls fan referència a una estació, a un determinat dia o a un contaminant però no s'ha detectat cap en concret. 
# Per eliminar els nuls interpolem els valors de les mesures no fetes amb altres valors de la mateixa fila, però diferent hora.
# 

# %%
#dataframe dels valors H

df_H = df.select_dtypes(include=[float])  
df_H.isna().sum() 
df_H.head(50)

# %% [markdown]
# Interpolem per files. Son valors d'hores consecutives, per tant entre un valor i un altre hauria d'haver una certa relació.

# %%
#calculem l'estadística abans d'interpolar, per comparar amb el valors finals
df_H.describe()

# %%
df_H.interpolate(method='linear', limit_direction='forward', axis=0,inplace=True)
df_H.isna().sum() #verifiquem nuls
df_H.describe() #calculem valors estadistics nous


# %%
sums=df_H.sum( axis=1)
df_H["Mitjana_diaria"]=sums/24
df_H.head()

# %% [markdown]
# Unim les dades H amb les dades d'estació, contaminant i dia del dataframe original

# %%
df_3 = pd.concat([df_1, df_H], axis=1)
df_3.describe()

# %%
#podem estudiar 8 estacions i 22 contaminants
df_3.nunique()

# %%
df_3.info()

# %% [markdown]
# Seleccionen el contaminant 8 (NO2)

# %%
df_c8= df_3[df_3["CODI_CONTAMINANT"] == 8]
df_c8.describe()
df_c8.head()
#df_c1.info()

# %%
df_c8.describe()

# %%
sns.boxplot(x='ESTACIO', y="Mitjana_diaria", data=df_c8)
plt.show()


# %% [markdown]
# Estudi de les mesures amb valors màxims

# %%
df_c8M= df_c8[df_c8["ESTACIO"] == 58]
df_c8M.describe()
df_c8M.head()

# %% [markdown]
# Mirem com varia el contaminant segons el dia

# %%
xpoints = df_c8M["DIA"]
ypoints = df_c8M["Mitjana_diaria"]

plt.plot(xpoints, ypoints)
plt.xlabel("dia del mes")
plt.ylabel("mesura del contaminant")
plt.title("Variació del contaminant segons el dia del mes")
plt.show()
"""
fig = plt.figure()
"""

"""


# %% [markdown]
# Seleccionamos segun dia de la semana laborable o no
# En octubre los fines de semana han sido: 1,7,8,14,15,21,22,28,29

# %%
df_c8MF= df_c8M[(df_c8M["DIA"] == 1)|(df_c8M["DIA"] == 7)|(df_c8M["DIA"] == 8)|(df_c8M["DIA"] == 14)|(df_c8M["DIA"] == 15)|(df_c8M["DIA"] == 21)|(df_c8M["DIA"] == 22)|(df_c8M["DIA"] == 28)|(df_c8M["DIA"] == 29)]
df_c8MF

# %%
df_c8MF.drop(['DIA',"ESTACIO","CODI_CONTAMINANT"], axis=1, inplace=True)
df_c8MF.head()
df_c8MF.plot(kind="box")
plt.xticks(rotation=90) #rotar els labels de l'eix x
plt.title("Variació contaminant segons hora del dia")


# %%
xpoints = df_c8M["DIA"]
ypoints = df_c8M["Mitjana_diaria"]

plt.plot(xpoints, ypoints)
plt.xlabel("dia del mes")
plt.ylabel("mesura del contaminant")
plt.title("Variació del contaminant segons el dia del mes")
plt.show()
fig = plt.figure()

# %%
df_c8ML= df_c8M[(df_c8M["DIA"] != 1)&(df_c8M["DIA"] != 7)&(df_c8M["DIA"] != 8)&(df_c8M["DIA"] != 14)&(df_c8M["DIA"] != 15)&(df_c8M["DIA"] != 21)&(df_c8M["DIA"] != 22)&(df_c8M["DIA"] != 28)&(df_c8M["DIA"] != 29)]
df_c8ML

# %%
df_c8ML.drop(['DIA',"ESTACIO","CODI_CONTAMINANT"], axis=1, inplace=True)
df_c8ML.head()
df_c8ML.plot(kind="box")
plt.xticks(rotation=90) #rotar els labels de l'eix x
plt.title("Variació contaminant segons hora del dia")


# %% [markdown]
# Estudiem l'estació on les mesures son més baixes (estació 58)

# %%
df_c8m= df_c8[df_c8["ESTACIO"] == 58]
df_c8m.describe()
df_c8m.head()

# %%
xpoints = df_c8m["DIA"]
ypoints = df_c8m["Mitjana_diaria"]

plt.plot(xpoints, ypoints)
plt.xlabel("dia del mes")
plt.ylabel("mesura del contaminant")
plt.title("Variació del contaminant segons el dia del mes")
plt.show()
fig = plt.figure()

# %%
df_c8m.drop(['DIA',"ESTACIO","CODI_CONTAMINANT"], axis=1, inplace=True)

df_c8m.plot(kind="box")
plt.xticks(rotation=90) #rotar els labels de l'eix x
plt.title("Variació contaminant segons hora del dia")


# %%
df.describe()

# %%
df1=df.copy()
df1.drop(["CODI_PROVINCIA","CODI_MUNICIPI","MUNICIPI","PROVINCIA","ANY","MES"],axis=1,inplace=True)
df1.head(5)

# %%
df2=df1.copy()
df3 = df2.select_dtypes(include=['float'])
df3
mitjana=df3.sum(axis=1)/24
mitjana


# %%

#df_temp3 = pd.concat([df_temp["Any"], mitjana], axis=1),"DIA","CODI_CONTAMINANT"

df4 = pd.concat([df1["DIA"],df1["ESTACIO"],df1["CODI_CONTAMINANT"], mitjana], axis=1)
df4.head()

# %%
df4.describe()

# %%
df5= df4[df4["CODI_CONTAMINANT"] == 9]

# %%
sns.countplot(x='ESTACIO', data=df5)
plt.xticks(rotation=90) #rotar els labels de l'eix x
plt.title("Nombre de dies detectat el Contaminant 7 per estacions de control")

# %%
sns.barplot(x='ESTACIO', y=0, data=df5)

# %%
sns.boxplot(x='ESTACIO', y=0, data=df5)

# %%
sns.pointplot(x="DIA",y=0,hue="ESTACIO",data=df5)

# %%
df6= df5[df5["ESTACIO"] == 50]
df6.head()
df6.describe()

# %%
sns.pointplot(x="DIA", y=0,data=df6)
plt.xticks(rotation=90) #rotar els labels de l'eix x
plt.title("Contaminant 7 per estacions de control")



"""

