import streamlit as st
import pandas as pd
import pickle
with open('optimisation_modele.pkl', 'rb') as file:
    optimisation_modele = pickle.load(file)
#st.set_page_config(layout="wide")
st.header("Data Mining : optimisation des prix")

col1, col2, col3, col4, col5, col6 = st.columns(6)

#Accommodates
accommodates = st.number_input("Entrez le nombre des invités", value=0)

#Bathrooms

bathrooms = st.number_input("Entrer le nombre de salles de bains", value=0)

#Bedrooms
bedrooms = st.number_input("Entrer le nombre des chambres à coucher", value=0)

#Guests included

guests = st.number_input("Entrer le nombre les invités inclus", value=0)

#Nombre des quartiers
quartiers_liste=['Ballard','Beacon Hill','Capitol Hill','Cascade','Central Area',
            'Delridge','Downtown','Interbay','Lake City','Magnolia','Northgate',
        'Queen Anne','Rainier Valley','Seward Park','University District','West Seattle',
            'Other neighborhoods']

quartiers_selecte = st.selectbox("Sélectionner le quartier",quartiers_liste, key='quartiers')

mois_liste = ['January','February','March','April','May','June','July',
        'August','September','October','November','December']
mois_selecte = st.selectbox("Sélectionner le mois",mois_liste, key='mois')

def prix_opt(accommodates,bathrooms,bedrooms,guests,quartiers_selecte,mois_selecte):
    if(accommodates>0 & bathrooms>=0 & bedrooms>=0 & guests>=0):
        accommodates = {'accommodates': accommodates}
        bathrooms = {'bathrooms': bathrooms}
        bedrooms = {'bedrooms': bedrooms}
        guests = {'guests_included': guests}
        quartiers = {quartiers:1 if quartiers==quartiers_selecte else 0 for quartiers in quartiers_liste}
    
    #in fitting the model i used this order of months so i need to keep it
        order = ['April', 'August', 'December', 'February', 'January', 'July', 'June', 
        'March', 'May', 'November', 'October', 'September']

        mois = {mois: 1 if mois == mois_selecte else 0 for mois in mois_liste}
        mois_dict = {mois_nom: mois[mois_nom] for mois_nom in order}
        data = {**accommodates, **bathrooms, **bedrooms, **guests, **quartiers, **mois_dict}

        data2 = pd.DataFrame([data], index=[0])
        prix = optimisation_modele.predict(data2)

        return prix
    else:
        return -1

if st.button("Offrez-moi les meilleurs prix !", type="primary"):
    #st.warning('This is a warning', icon="🤖")
    prix = prix_opt(accommodates,bathrooms,bedrooms,guests,quartiers_selecte,mois_selecte)
    if prix == -1:
        st.warning('Vérifiez si des nombres sont négatifs ou si le nombre des invités est égal à zéro.', icon="🤖")
    else:
        st.success(f'Voilà les meilleurs prix : {"{:.2f}".format(prix[0])} || {"{:.2f}".format(prix[0]+10)}  ||  {"{:.2f}".format(prix[0]-10)}', icon="✅")