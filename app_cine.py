import streamlit as st
import numpy as np
import pandas as pd
#import requests
#from sklearn.neighbors import NearestNeighbors
#from sklearn.preprocessing import StandardScaler
#from sklearn.preprocessing import MinMaxScaler

# import des fichiers
df_films = pd.read_pickle("df_noms_films.pkl.gz", compression = 'gzip')
df_genres = pd.read_pickle("df_genres.pkl.gz", compression = 'gzip')
df_acteurs = pd.read_pickle('df_noms_acteurs.pkl.gz', compression = 'gzip')
#df_annees = pd.read_pickle('df_annees.pkl.gz', compression = 'gzip')
df_final = pd.read_pickle('df_merge_final_ML.pkl.gz', compression = 'gzip')

# récupération des colonnes intéressantes pour le ML
df_final2 = df_final.copy(deep= True)
#df_final2[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']] = StandardScaler().fit_transform(df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']])
df_final2[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']] = MinMaxScaler().fit_transform(df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']])

df_test = df_final2.iloc[:, 4:]

#df_test = df_final.iloc[:, 8:]

# A FAIRE
# Préciser que toutes les colonnes sont de la même importance et de la même grandeur
# Scale data
#scaler = StandardScaler().fit(X)
# X_scaled = scaler.transform(X)


X = df_test[list(df_test.columns)]

#scaler = StandardScaler().fit(X)
#X_scaled = scaler.transform(X)

# Entraînement du modèle, sur les 4 plus proches (donc les 3)
#distanceKNN = NearestNeighbors(n_neighbors = 4).fit(X_scaled)
#distanceKNN = NearestNeighbors(n_neighbors = 4).fit(X)
#distanceKNN = NearestNeighbors(n_neighbors = 4, metric = "cosine", algorithm = "brute").fit(X)

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

liste_films = ['Entre ton film préféré'] + list(df_films['primaryTitle'].map(str) + ' (' + df_films['startYear'].map(str) + ')')
    #df_films['primaryTitle'] + ' (' + str(df_films['startYear']) + ')')

#url_imdb = "https://www.imdb.com/title/tt0006206/"
#url_imdb = "https://m.media-amazon.com/images/M/MV5BMTc1NTY3NDIzNl5BMl5BanBnXkFtZTgwNTIyODg5MTE@._V1_QL75_UY281_CR6,0,190,281_.jpg"

key_api = "&apikey=79204f79"
url_api = "http://www.omdbapi.com/?i="


with st.form('form_1'):
    films = st.selectbox("Film : ",
                           liste_films)
    films_titre = films[:-7]
    try:
        films_annee = int(films[-5:-1])
    except:
        films_annee = 0
        
    submit1 = st.form_submit_button("OK !")
    
if submit1 and (films != 'Entre ton film préféré'):
    st.write(f'Avec le film {films_titre} ({films_annee}) , je te suggère fortement de regarder les films :')    
    film_choisi = df_final2[((df_final['primaryTitle'] == films_titre) & (df_final['startYear'] == films_annee) )
                           | ((df_final['originalTitle'] == films_titre)  & (df_final['startYear'] == films_annee))
                           | ((df_final['frenchTitle'] == films_titre) & (df_final['startYear'] == films_annee))
                          ]
    
    film_choisi = film_choisi.iloc[0:1, 4:]
    #st.write(film_choisi)
    #neighbors = distanceKNN.kneighbors(film_choisi)
    #films_titre_fr = df_final.iloc[neighbors[1][0][1:]]['frenchTitle'].values
    #films_titre_origine = df_final.iloc[neighbors[1][0][1:]]['primaryTitle'].values
    #tconsts =  df_final.iloc[neighbors[1][0][1:]]['tconst'].values
    #annees = df_final.iloc[neighbors[1][0][1:]]['startYear'].values
    #for tconst1, titre in zip(tconst, films_bons):
    #    st.write(' {} - {}'.format(tconst1, titre))
    #st.image(url_imdb, width=100)

    #colfilms = st.columns(3)
    #for cols, tconst, titre_fr, titre_eng, annee in zip(colfilms, tconsts, films_titre_fr, films_titre_origine, annees):
        #with cols:            
        
            #url = url_api + str(tconst) + key_api
            #try:
            #    response = requests.get(url)
            #    response.raise_for_status()
            #    data = response.json()
            #    url_image = data['Poster']
            #    st.image(url_image, width=200)
            #except requests.exceptions.RequestException as e:
            #    print('Une erreur est survenue lors de l\'appel à l\'API :', e)
            # parfois il n'existe pas de titre en français
            #if type(titre_fr) == str:
            #    st.write(f' - {titre_fr} ({annee})')
            #else:
            #    st.write(f' - {titre_eng} ({annee})')
            

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
                                  options = range(1913,2024),
                                  value = (1913, 2023))
                                   

    submit = st.form_submit_button("C'est parti !")

if submit:
    #if annees != 'pas de préférence':
    #    st.write(np.random.choice(phrases_annees).format(annees))
    film_choisi2 = df_final        
    if genres:
        st.write(np.random.choice(phrases_genres).format('/'.join(genres)))   
        #for genre in genres:
        #    film_choisi2 = film_choisi2[(film_choisi2['genres'] == genre) | (df_final['originalTitle']==films)]        
    if acteurs != '':
        st.write(np.random.choice(phrases_acteurs).format(acteurs))
        film_choisi2 = film_choisi2[film_choisi2[acteurs] == True]

    
    st.write("Avec le(s) genre {}, l'acteur/actrice {} et les années {}\n je te suggère fortement :".format("/".join(genres), acteurs, str(debut_an) +'-'+ str(fin_an)))

    #film_choisi2 = df_final[(df_final['primaryTitle'] == films) | (df_final['originalTitle']==films)]
    df_final2 = film_choisi2.iloc[:,:]
    df_test2 = df_final2.iloc[:,5:]
    #st.write(film_choisi2.iloc[:,:5])#df_test2
    film_choisi2 = film_choisi2.iloc[0:1,5:]
    X2 = df_test2[list(df_test2.columns)]
    #distanceKNN2 = NearestNeighbors(n_neighbors = 4).fit(X2)
    #neighbors2 = distanceKNN2.kneighbors(film_choisi2)
    #neighbors2
    #films_bons2 = df_final2.iloc[neighbors2[1][0][:], 1].values
    #tconsts2 =  df_final2.iloc[neighbors2[1][0][:], 0].values

    #colfilms2 = st.columns(3)
    #for cols, tconst, titre in zip(colfilms2, tconsts2, films_bons2):
        #st.write(tconst, titre)
        #with cols:            
        
            #url2 = url_api + str(tconst) + key_api
            #try:
            #    response2 = requests.get(url2)
            #    response2.raise_for_status()
            #    data2 = response2.json()
            #    url_image2 = data2['Poster']
            #    st.image(url_image2, width=200)
                
            #except requests.exceptions.RequestException as e:
            #    print('Une erreur est survenue lors de l\'appel à l\'API :', e)
            #st.write(' - {} '.format(titre))
