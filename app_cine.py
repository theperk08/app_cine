import streamlit as st
import numpy as np
import pandas as pd
import requests
from sklearn.neighbors import NearestNeighbors
#from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
#import hydralit_components as hc


    
#cd Documents\Wild_Code_School\Projets\Projet_2_Cinema
# streamlit run app_cine_ML.py

# import des fichiers
df_films = pd.read_pickle("df_noms_films2.pkl.gz", compression = 'gzip')
df_genres = pd.read_pickle("df_genres.pkl.gz", compression = 'gzip')
df_acteurs = pd.read_pickle('df_noms_acteurs.pkl.gz', compression = 'gzip')
#df_annees = pd.read_pickle('df_annees.pkl.gz', compression = 'gzip')
df_final = pd.read_pickle('df_merge_final_ML2.pkl.gz', compression = 'gzip')

# récupération des colonnes intéressantes pour le ML

#df_final2 = df_final.copy(deep= True)

print('debut')

df_annees = df_final[['tconst', 'startYear']]

scaling = MinMaxScaler()
scaling.fit(df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']])

#df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']] = StandardScaler().fit_transform(df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']])
df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']] = scaling.transform(df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']])

df_test = df_final.iloc[:, 4:]

print(len(df_test))

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

print('fit X')
distanceKNN = NearestNeighbors(n_neighbors = 4, metric = "cosine", algorithm = "brute").fit(X)
print('fin fit X')

st.set_page_config(
  page_title = "Ex-stream-ly Cool App",
  layout = "wide",
  page_icon = "🎞️")

#Mise en forme fond de page

page_bg_img = """
<style>
[data-testid = "stAppViewContainer"] {

background-color: #e5e5f7;
opacity: 0.8;
#background-image: ;
background-size: 10px 10px;

}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html = True)
  
phrases_acteurs = ['Tu aimes vraiment {} ?', "{} n'est pas mon acteur/actrice préféré(e) mais je respecte ton choix", "Moi aussi j'adore {} !"]

phrases_annees = ["Ah, c'était vraiment chouette les années {}", "Toi aussi t'as un très bon souvenir des années {} ?", "Bof, on a connu mieux que les années {}"]

phrases_genres = ["J'adore le genre {}", "Le style {} n'est pas mon préféré", "Pas terribles les {}"] 

phrases_alea = ["Avec le film {}, du genre {}, l'acteur/actrice {} et l'année {}\n je te suggère fortement :",
                "T'as pas honte d'avoir regardé le film {} ?",
                "Très bon choix l'acteur {}",
                "C'était chouette les années {}"
               ]

st.title("Dis-moi ton film préféré :clapper: et je t'en ferai aimer encore d'autres ! :popcorn:")

#liste_films = ['Entre ton film préféré'] + list(df_films['primaryTitle'].map(str) + ' (' + df_films['startYear'].map(str) + ')')
liste_films = ['Entre ton film préféré'] + list(df_films['primaryTitle'].map(str))

    #df_films['primaryTitle'] + ' (' + str(df_films['startYear']) + ')')

#url_imdb = "https://www.imdb.com/title/tt0006206/"
#url_imdb = "https://m.media-amazon.com/images/M/MV5BMTc1NTY3NDIzNl5BMl5BanBnXkFtZTgwNTIyODg5MTE@._V1_QL75_UY281_CR6,0,190,281_.jpg"

key_api = "&apikey=79204f79"
url_api = "http://www.omdbapi.com/?i="

url_title = 'https://www.imdb.com/title/'

print('debut forme')
with st.form('form_1'):
    films = st.selectbox("Film : ",
                           liste_films)
    #films_titre = films[:-7]
    #try:
    #    films_annee = int(films[-5:-1])
    #except:
    #    films_annee = 0
        
    submit1 = st.form_submit_button("OK !")
    
if submit1 and (films != 'Entre ton film préféré'):
    with st.spinner('Un instant, ça arrive...'):
        st.subheader(f'Avec le film {films}, je te suggère fortement de regarder les films :')    
        #film_choisi = df_final2[((df_final['primaryTitle'] == films_titre) & (df_final['startYear'] == films_annee) )
        #                       | ((df_final['originalTitle'] == films_titre)  & (df_final['startYear'] == films_annee))
        #                       | ((df_final['frenchTitle'] == films_titre) & (df_final['startYear'] == films_annee))
        #                      ]

        #film_choisi = df_final[(df_final['primaryTitle'] == films) #_titre )
        #                       | (df_final['originalTitle'] == films) #_titre) )
        #                       | (df_final['frenchTitle'] == films)] #_titre))

        #st.write(liste_films.index(films))
        #st.write(df_films.iloc[liste_films.index(films) - 1 ])

        film_choisi = df_final[df_final['tconst'] == df_films.iloc[liste_films.index(films) - 1 ]['tconst']] #_titre )



        film_choisi = film_choisi.iloc[0:1, 4:]
        #st.write(film_choisi)
    
    # a dedicated single loader 
   
   
        neighbors = distanceKNN.kneighbors(film_choisi)
        films_titre_fr = df_final.iloc[neighbors[1][0][1:]]['frenchTitle'].values
        films_titre_origine = df_final.iloc[neighbors[1][0][1:]]['primaryTitle'].values
        tconsts =  df_final.iloc[neighbors[1][0][1:]]['tconst'].values
        annees = df_final.iloc[neighbors[1][0][1:]]['startYear'].values
        #for tconst1, titre in zip(tconst, films_bons):
        #    st.write(' {} - {}'.format(tconst1, titre))
        #st.image(url_imdb, width=100)

        colfilms = st.columns(3)
        for cols, tconst, titre_fr, titre_eng, annee in zip(colfilms, tconsts, films_titre_fr, films_titre_origine, annees):
            with cols:            

                url = url_api + str(tconst) + key_api
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    url_image = data['Poster']
                    st.image(url_image, width=200)
                except requests.exceptions.RequestException as e:
                    print('Une erreur est survenue lors de l\'appel à l\'API :', e)
                # parfois il n'existe pas de titre en français
                url_fr = url_title + str(tconst)
                if type(titre_fr) == str:                    
                    st.write(f' - [{titre_fr}]({url_fr})')
                else:
                    st.write(f' - [{titre_eng}]({url_fr})')



            
st.subheader('Tu peux aussi éventuellement choisir parmi au moins un genre ou un acteur :')

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
                                   

    submit2 = st.form_submit_button("C'est parti !")
    
    
 
    

if submit2:
    #if annees != 'pas de préférence':
    #    st.write(np.random.choice(phrases_annees).format(annees))
    film_choisi2 = df_final.copy()
    
    #st.write('data final', len(film_choisi2))
    
    
    #st.write(debut_an, fin_an)
   
    film_choisi_annees = pd.merge(df_annees[df_annees['startYear'].between(debut_an, fin_an)], film_choisi2, how = 'left', left_on = 'tconst', right_on = 'tconst')
    #film_choisi2 = film_choisi2.drop(columns = 'startYear_x')
    #film_choisi2 = film_choisi2.rename(columns = {'startYear_y' : 'startYear'})
                                                                                     
    
    #st.write('longueur data années', len(film_choisi_annees))
    
    if genres:
        #st.write(np.random.choice(phrases_genres).format('/'.join(genres)))   
        #genres_choisis = '|'.join(genres)
        #film_choisi2 = film_choisi2[film_choisi2['genres'].str.contains(genres_choisis)]
        film_choisi_genres =  pd.DataFrame()
        for genre in genres:            
            film_choisi_genres = pd.concat([film_choisi_genres, film_choisi_annees[film_choisi_annees[genre] == True]])
        film_choisi_genre_annees = film_choisi_genres.drop_duplicates()
    
    #st.write('longueur data genres', len(film_choisi_genre_annees))
    
    
                                    
    if acteurs != '':
        #st.write(np.random.choice(phrases_acteurs).format(acteurs))
        film_choisi_acteurs = film_choisi2[film_choisi2[acteurs] == True]
    
    #st.write('longueur data acteurs', len(film_choisi_acteurs))

    
    
    #st.write(film_choisi2)
    #film_choisi2 = df_final[(df_final['primaryTitle'] == films) | (df_final['originalTitle']==films)]
    #df_final2 = film_choisi2.iloc[:,:]
    #df_test2 = df_final2.iloc[:, 4:]
    #st.write(film_choisi2.iloc[:,:5])#df_test2
    #film_choisi2 = film_choisi2.iloc[0:1, 4:]
    #X2 = df_test2[list(df_test2.columns)]
    #distanceKNN2 = NearestNeighbors(n_neighbors = 4).fit(X2)
    #distanceKNN2 = NearestNeighbors(n_neighbors = 4, metric = "cosine", algorithm = "brute").fit(X)
    #neighbors2 = distanceKNN2.kneighbors(film_choisi2)
    #neighbors2
    #films_bons2 = df_final2.iloc[neighbors2[1][0][:], 1].values
    #tconsts2 =  df_final2.iloc[neighbors2[1][0][:], 0].values

    # PAS DE MACHINE LEARNING,
    
     # TOP 3 basé sur AverageRating à partir choix : acteur
    if acteurs != '':
    
        st.subheader("Puisque tu adores l'acteur/actrice {}, je te suggère fortement :".format(acteurs))
                
        top_3 = film_choisi_acteurs.sort_values(by = 'averageRating', ascending = False).iloc[:3, :]
        top_3_consts = top_3.iloc[:3, 0]
        top_3_titres_fr = top_3.iloc[:3]['frenchTitle'] 
        top_3_titres_eng = top_3.iloc[:3]['originalTitle']
        top_3_annees = top_3.iloc[:3]['startYear']
                    
        colfilms_acteur = st.columns(3)
        for cols, tconst, titre_fr, titre_eng, annees in zip(colfilms_acteur, top_3_consts, top_3_titres_fr, top_3_titres_eng, top_3_annees):
            #st.write(tconst, titre)
            with cols:            
        
                url2 = url_api + str(tconst) + key_api
                try:
                    response2 = requests.get(url2)
                    response2.raise_for_status()
                    data2 = response2.json()
                    url_image2 = data2['Poster']
                    st.image(url_image2, width=200)
                
                except requests.exceptions.RequestException as e:
                    print('Une erreur est survenue lors de l\'appel à l\'API :', e)
                    
                url_fr = url_title + str(tconst)
                if type(titre_fr) == str:                    
                    st.write(f' - [{titre_fr}]({url_fr})')
                else:
                    st.write(f' - [{titre_eng}]({url_fr})')

                
                    
    
    # TOP 3 basé sur AverageRating à partir choix : genres et années
    
    if genres != []:
        st.subheader("Avec le(s) genre {}, et les années {}, je te suggère fortement :".format("/".join(genres), str(debut_an) +'-'+ str(fin_an)))

        top_3 = film_choisi_genre_annees.sort_values(by = 'averageRating', ascending = False).iloc[:3, :]
        top_3_consts = top_3.iloc[:3, 0]
        top_3_titres_fr = top_3.iloc[:3]['frenchTitle'] 
        top_3_titres_eng = top_3.iloc[:3]['originalTitle']
        top_3_annees = top_3.iloc[:3]['startYear_x']


        colfilms2 = st.columns(3)
        for cols, tconst, titre_fr, titre_eng, annees in zip(colfilms2, top_3_consts, top_3_titres_fr, top_3_titres_eng, top_3_annees):
            #st.write(tconst, titre)
            with cols:            

                url2 = url_api + str(tconst) + key_api
                try:
                    response2 = requests.get(url2)
                    response2.raise_for_status()
                    data2 = response2.json()
                    url_image2 = data2['Poster']
                    if len(url_image2) > 0:
                        st.image(url_image2, width=200)

                except requests.exceptions.RequestException as e:
                    print('Une erreur est survenue lors de l\'appel à l\'API :', e)

                url_fr = url_title + str(tconst)
                if type(titre_fr) == str:                    
                    st.write(f' - [{titre_fr}]({url_fr})')
                else:
                    st.write(f' - [{titre_eng}]({url_fr})')


                
    
                    

    