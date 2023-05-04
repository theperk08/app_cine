import streamlit as st
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# import des fichiers
df_films = pd.read_pickle("df_noms_films.pkl.gz", compression = 'gzip')
df_genres = pd.read_pickle("df_genres.pkl.gz", compression = 'gzip')
df_acteurs = pd.read_pickle('df_noms_acteurs.pkl.gz', compression = 'gzip')
df_annees = pd.read_pickle('df_annees.pkl.gz', compression = 'gzip')
df_final = pd.read_pickle('df_merge_final_ML.pkl.gz', compression = 'gzip')

# récupération des colonnes intéressantes pour le ML
df_test = df_final.iloc[:, 5:]

# Entraînement du modèle, sur les 4 plus proches (donc les 3)
X = df_test[list(df_test.columns)]
distanceKNN = NearestNeighbors(n_neighbors = 4).fit(X)



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
#submit1 = st.form_submit_button("OK !")

st.write('Tu peux aussi éventuellement choisir parmi :')

liste_genres = [''] + list(df_genres['genres'])
liste_acteurs = [''] + list(df_acteurs['primaryName'])

with st.form("form 2"):
    col1, col2, col3 = st.columns(3)

    with col1:
        genres = st.multiselect(label = "Genres :", options = liste_genres)
    with col2:
        acteurs = st.selectbox("Acteur :",
                               liste_acteurs)        
    
    with col3:
        debut_an, fin_an = st.select_slider("Sélectionne une fourchette d'années",
                                  options = df_annees['startYear'],
                                  value = (1980, 1990))
                                   

    submit = st.form_submit_button("C'est parti !")

if submit:
    #if annees != 'pas de préférence':
    #    st.write(np.random.choice(phrases_annees).format(annees))        
    if genres:
        st.write(np.random.choice(phrases_genres).format('/'.join(genres)))        
    if acteurs != '':
        st.write(np.random.choice(phrases_acteurs).format(acteurs))  
    
    st.write("Avec le(s) genre {}, l'acteur/actrice {} et les années {}\n je te suggère fortement :".format(films, "/".join(genres), acteurs, str(debut_an) +'-'+ str(fin_an)))
    
#film_choisi = df_final[(df_final['primaryTitle'] == films) | (df_final['originalTitle']==films)]
#film_choisi = film_choisi.iloc[:,5:]    
#neighbors = distanceKNN.kneighbors(film_choisi)
#if submit1:
st.write('Avec le film {} , je te suggère fortement de regarder les films :'.format(films))
#for i in range(1,5):
#    film_bon = df_final.iloc[neighbors[1][0][i], 1]
#    st.write(' - '.format(film_bon))
