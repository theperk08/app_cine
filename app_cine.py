import streamlit as st
import numpy as np
import pandas as pd

df_films = pd.read_pickle("df_noms_films.pkl.gz", compression = 'gzip')
df_genres = pd.read_pickle("df_genres.pkl.gz", compression = 'gzip')
df_acteurs = pd.read_pickle('df_noms_acteurs.pkl.gz', compression = 'gzip')




st.set_page_config(
  page_title = "Ex-stream-ly Cool App",
  layout = "wide",
  page_icon = "🎞️")
  
phrases_acteurs = ['Tu aimes vraiment {} ?', "{} n'est pas mon acteur/actrice préféré(e) mais je respecte ton choix", "Moi aussi j'adore {} !"]

phrases_annees = ["Ah, c'était vraiment chouette les années {}", "Toi aussi t'as un très bon souvenir des années {} ?", "Bof, on a connu mieux que les années {}"]

phrases_genres = ["J'adore le genre {}", "Le style {} n'est pas mon préféré", "Pas terribles les {}"] 

phrases_alea = ["Avec le film {}, du genre {}, l'acteur/actrice {} et l'année {}\n je te suggère fortement :",
                "T'as pas honte d'avoir regardé le film {} ?",
                "Très bon choix l'acteur {}",
                "C'était chouette les années {}"
               ]

st.title("Dis-moi ton film préféré et je t'en ferai aimer encore d'autres !!!")

liste_films = ['Entre ton film préféré'] + list(df_films['primaryTitle'])
films = st.selectbox("Film : ",
                     liste_films)

st.write('Tu peux aussi éventuellement choisir parmi :')

liste_genres = [''] + list(df_genres['genres'])
liste_acteurs = [''] + list(df_acteurs['primaryName'])

with st.form("form 2"):
    col1, col2, col3 = st.columns(3)

    with col1:
        genres = st.multiselect(label = "Genres :", options = liste_genres, default = "rien")
    with col2:
        acteurs = st.selectbox("Acteur :",
                               liste_acteurs)        
    
    with col3:  
        annees = st.radio("Années",
    ('pas de préférence', '1910-1920', '1920-1930', '1930-1940', '1940-1950', '1950-1960', '1960-1970', '1970-1980', '1980-1990', '1990-2000', '2000-2010', '2010-2020', '2020-'), index = 0 )
        

    submit = st.form_submit_button("Submit")

# print the selected hobby
if submit:
    
    if annees != 'pas de préférence':
        st.write(np.random.choice(phrases_annees).format(annees))
        
    if genres:
        st.write(np.random.choice(phrases_genres).format('/'.join(genres)))
        
    if acteurs != '':
        st.write(np.random.choice(phrases_acteurs).format(acteurs))
        
    
    
    st.write("Avec les films {}, du genre {}, l'acteur/actrice {} et les années {}\n je te suggère fortement :".format(films, "/".join(genres), acteurs, annees))
    
        
#x = st.slider('Select a value')
#st.write(x, 'squared is', x * x)
