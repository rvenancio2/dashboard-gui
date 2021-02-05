import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

DATA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS0LE_5WZpBd7Cl2chlto0yJLT3eWhOj73To_o-6qVqGWSVIg7WwUQ8Sq2tFuiOXhxvqKXKJ_6M6Hf9/pubhtml"

def crises_dia(param):
    fig, ax1 = plt.subplots(1,1,figsize=(10,10))
    #fig, (ax1, ax2) = plt.subplots(1,2,figsize=(20,6))        
    temp_df  = (pd.to_datetime(df[df['evento'] == 'Crise']['hora_final'])
    .dt.floor('d')
    .value_counts()
    .rename_axis('Dia')
    .reset_index(name='Total'))
    
    temp_df['Dia'] = temp_df['Dia'].dt.strftime('%m/%d')
    temp_df.sort_values(by=[param], inplace=True)
    
    splot = sns.barplot(x="Dia", y="Total", data=temp_df, ax=ax1)
    ax1.set_ylabel('Scores')    
    ax1.legend()

    for p in splot.patches:
        splot.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    size=15,
                    xytext = (0, -12), 
                    textcoords = 'offset points')
    
    st.pyplot(fig)
    
def load_data():
    df = pd.read_html(DATA_URL, header=1)[0]
    df.drop(columns='1', inplace=True)

    df.columns = ['timestamp', 'hora_reportada', 'hora_final', 'evento_onde','evento', 
             'tipo_crise', 'antes_crise',  'durante_crise',
             'comidas',
             'remedios',
             'valor_cetose',
             'email',
             'depois_crise'             
             ]
            
    df = df[1:]        
    df['hora_final'] = np.where(df['hora_reportada'].isna(), df["timestamp"], df["hora_reportada"])
    df.drop('timestamp', axis=1, inplace=True)
    df.drop('hora_reportada', axis=1, inplace=True)
    return df

df = load_data()

st.title("Caderno digital de Guilherme")
st.markdown(
    f"""
    Dashboard para analise do dia a dia de Guilherme.    
    Carregando {df.shape[0]} linhas com eventos de entrada.    
    """)

# Raw Data
st.sidebar.header("Configuracoes")
page = st.sidebar.selectbox(
    'Selecionar Dashboard',
    ('Pagina Principal', 'Eventos por Local', 'Crises por Dia'))

#st.write('You selected:', page)
#if st.sidebar.checkbox("Mostrar Raw Data"):
    #st.write(df)

if page == 'Pagina Principal':
    st.markdown('Dados')
if page == 'Eventos por Local':
    fig, ax1 = plt.subplots()
    #fig, (ax1, ax2) = plt.subplots(1,2,figsize=(20,6))
    splot = sns.countplot(x="evento_onde", data=df, ax = ax1)
    #sns.countplot(x="evento_onde", data=df, ax = ax2)
    for p in splot.patches:
        splot.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    size=15,
                    xytext = (0, -12), 
                    textcoords = 'offset points')
    st.pyplot(fig)

if page == 'Crises por Dia':
    st.title("Quantidade de crises por dia")
    orderby = st.radio("Ordenados por:", ('Dia', 'Quantidade'))
    if orderby == 'Dia':
        crises_dia('Dia')
    else:
        crises_dia('Total')



    


