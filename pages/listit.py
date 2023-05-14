import streamlit as st 
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from geopy.geocoders import Nominatim
from features import features_detected
from geografia_to_provincia import return_province


def find_top_five_houses(new_house, df):
    """Returns top 5 most similar houses in dataframe"""

    # primer fem amb les propietats importants
    df_houses = df[new_house.price < df.price*1.17]
    
    similarity_scores_200 = cosine_similarity(new_house[["price","square_meters", "bedrooms", "bathrooms", "image_data.r1f6.property"]], df_houses[["price","square_meters", "bedrooms", "bathrooms", "image_data.r1f6.property"]]) # afegir noms columnes
    most_similar_indexes_200 = similarity_scores_200.argsort()[0,::-1][:200]
    top_similar_houses_200 = df.loc[most_similar_indexes_200]
    
    similarity_scores_5 = cosine_similarity(new_house, top_similar_houses_200)
    most_similar_indexes_5 = similarity_scores_5.argsort()[0,::-1][:5]
    top_similar_houses_5 = df.loc[most_similar_indexes_5]

    return top_similar_houses_5




def main():

    # Customize app

    st.set_page_config(layout="wide")

    title_style = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans&display=swap');

            .centered-title {
                text-align: center;
                font-family: 'Josefin Sans', sans-serif;
            }
        </style>
    """

    st.markdown(title_style, unsafe_allow_html=True)
    margins_css = """
        <style>
            .appview-container .main .block-container{
                background-color:#f6c89c;
            }
        </style>
    """

    st.markdown("<h1 class='centered-title' style='background-color:#F1F1F1'>List it</h1>", unsafe_allow_html=True)

    st.markdown(margins_css, unsafe_allow_html=True)

    # Input del que volem
    price = st.number_input("Precio", min_value = 0)

    location_string = st.text_input("Localización")
    geolocator = Nominatim(user_agent="geoapiExercises")
    address = geolocator.geocode(location_string)

    square_meters = st.number_input("Metros cuadrados (aproximado)", min_value = 0)

    num_bathrooms = st.slider("Número de baños (aproximado)", 0, 15, 0)
    num_bedrooms = st.slider("Número de habitaciones (aproximado)", 0, 20, 0)

    r1f6 = st.selectbox("Score Propiedad", ("Disrepair", "Poor", "Average", "Good", "Excellent", "Luxury"))

    options = st.multiselect(
    'Otros atributos que valoraría positivamente', features_detected
    )
    
    # clicar botó GO
    if st.button("GO"):
        if price == 0:
            st.write("¡Falta el precio!")
        elif location_string == "":
            st.write("¡Falta la localización!")
        elif square_meters == 0:
            st.write("¡Faltan la superficie!")
        elif num_bathrooms == 0:
            st.write("¡Falta el número de baños!")
        elif num_bedrooms == 0:
            st.write("¡Falta el número de habitaciones!")
            
        else:  # find ideal house
            new_row = {"square_meters":[square_meters],
            "num_images":[11],
            "image_data.r1f6.property" : [r1f6 if r1f6 != 0 else 3]}

            for el in features_detected:
                if el in options:
                    new_row[el] = 1
                else:
                    new_row[el] = 0.65

            new_row["logprice"] = np.log(price)

            new_row["property_type_numeric"] = 0.5

            # list_provinces = return_province(address.longitude, address.latitude)
            # for i in range(len(list_provinces)):
            #     if list_provinces[i] == True:
            #         new_row["id_prov_" + str(i) + ".0"] = 1
            #     else:
            #         new_row["id_prov_" + str(i) + ".0"] = 0

            desired_house = pd.DataFrame.from_dict(new_row)

            df = pd.read_csv("final_house_dataframe.csv")
            df = df.drop("Unnamed: 0", axis=1)

            top_five_houses = find_top_five_house(desired_house, df) # retorna la ubicació en el dataframe crec ???
            print(top_five_houses)



if __name__ == "__main__":
    main()
