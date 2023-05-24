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
df_final = pd.read_pickle('df_merge_final_ML3.pkl.gz', compression = 'gzip')

# récupération des colonnes intéressantes pour le ML

#df_final2 = df_final.copy(deep= True)

print('debut')

df_annees = df_final[['tconst', 'startYear']]

#scaling = MinMaxScaler()
#scaling.fit(df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']])

#df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']] = StandardScaler().fit_transform(df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']])
df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']] = MinMaxScaler().fit_transform(df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']])
#df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']] = scaling.transform(df_final[['startYear', 'runtimeMinutes', 'averageRating', 'numVotes']])

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


liste_films = ['Entre ton film préféré'] + list(df_films['primaryTitle'].map(str))
liste_genres = [''] + list(df_genres['genres'])
liste_acteurs = [''] + list(df_acteurs['primaryName'])




key_api = "&apikey=79204f79"
url_api = "http://www.omdbapi.com/?i="

url_title = 'https://www.imdb.com/title/'

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
  

st.title("Dis-moi ton film préféré :clapper: et je t'en ferai aimer encore d'autres ! :popcorn:")

#liste_films = ['Entre ton film préféré'] + list(df_films['primaryTitle'].map(str) + ' (' + df_films['startYear'].map(str) + ')')


print('debut forme')
colf1, colf2, colf3 = st.columns(3)

with colf2:
    with st.form('form_1'):
        films = st.selectbox("Film : ",
                               liste_films)
   
        submit1 = st.form_submit_button("OK !")
    
if submit1 and (films != 'Entre ton film préféré'):
    with st.spinner('Un instant, ça arrive...'):
        tconst_choisi = df_films.iloc[liste_films.index(films) - 1 ]['tconst']
        url = url_api + str(tconst_choisi) + key_api
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            url_image = data['Poster']
            st.image(url_image, width=200)
        except requests.exceptions.RequestException as e:
            print('Une erreur est survenue lors de l\'appel à l\'API :', e)
                
        url_fr = url_title + str(tconst_choisi)
        
        with colf2:
        
            st.subheader(f'Avec le film [{films}]({url_fr}), je te suggère fortement de regarder les films :')    
            film_choisi = df_final[df_final['tconst'] == df_films.iloc[liste_films.index(films) - 1 ]['tconst']] #_titre )
            film_choisi = film_choisi.iloc[0:1, 4:]
      
            neighbors = distanceKNN.kneighbors(film_choisi)
            films_titre_fr = df_final.iloc[neighbors[1][0][1:]]['frenchTitle'].values
            films_titre_origine = df_final.iloc[neighbors[1][0][1:]]['primaryTitle'].values
            tconsts =  df_final.iloc[neighbors[1][0][1:]]['tconst'].values
            annees = df_final.iloc[neighbors[1][0][1:]]['startYear'].values
        

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
   
    if genres != []:
        
        film_choisi_genres =  pd.DataFrame()
        for genre in genres:            
            film_choisi_genres = pd.concat([film_choisi_genres, film_choisi_annees[film_choisi_annees[genre] == True]])
        film_choisi_genre_annees = film_choisi_genres.drop_duplicates()
    
                                    
    if acteurs != '':
        
        film_choisi_acteurs = film_choisi2[film_choisi2[acteurs] == True]
    

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

