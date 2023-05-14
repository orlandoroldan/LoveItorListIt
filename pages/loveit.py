import streamlit as st 
import json
import pandas as pd
from features import *
from sklearn.preprocessing import LabelEncoder
import joblib
import requests

most_important_features = ["image_data.r1f6.property", "pool", "vanity", "fireplace", "double_sink", "tv", "hardwood_floor", "mirror", "dishwasher", "floor_ceiling_windows", "microwave", "notable_chandelier", "pergola", "shower", "kitchen_island", "outdoor_bar", "oven", "radiator", "built_in_shelves","refrigerator"]


def extract_image_data(file, old_house):

    solutions = file["response"]["solutions"]
    # r1r6
    old_house["image_data.r1f6.property"] = solutions['re_condition_r1r6_international']["score"]

    detections = solutions["re_features_v4"]["detections"]

    for element in features_detected:
        old_house[element] = 0

    for dictionary in detections:
        element = dictionary["label"]
        if element in features_detected:
            old_house[element] = 1



def comparison(old_house):
    """
    Mira quines important features falten
    """
    not_in_house = []
    i = 0

    for c in most_important_features[1:]:
        if old_house[c][0] == 0:
            not_in_house.append(c)
            i += 1
        if i == 5:
            break
    return not_in_house


def main():

    # config app beautiful
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
                background-color:#D8BFD8;
            }
        </style>
    """

    st.markdown("<h1 class='centered-title' style='background-color:#F1F1F1'>Love it</h1>", unsafe_allow_html=True)

    st.markdown(margins_css, unsafe_allow_html=True)

    # Llegir a través de links d'imatges una propietat

    txt_url = st.text_area("URL de imágenes. \nSeparar con Enter, no dejar espacios en blanco.")
    list_url = txt_url.split("\n")
    ubi = st.text_input("Ubicación")
    descrip = st.text_input("Descripción")
    num_baños = st.slider("Número de baños", 0,15,0)
    num_hab = st.slider("Número de habitaciones", 0, 20, 0)
    sq_meters = st.number_input("Metros cuadrados")
    num_images = len(list_url)
    property_type = option = st.selectbox(
        "¿De qué tipo de propiedad se trata?",
        ("Familiar", "Condo")
    )

    # la idea seria que poguessis pujar imatges, de moment farem servir urls
    # la resta de propietats les troba la API de restb.ai
    st.markdown("""
        <style>
        [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
            gap: 0rem;
        }
        </style>
        """,unsafe_allow_html=True)

    if st.checkbox("Recomendar Upgrades"):
        ###  Aquí cridem API de restb.ai i ens retornarà totes les features que necessitem
        list_models = ["re_features_v4", "re_condition_r1r6_international"]

        url = 'https://api-eu.restb.ai/vision/v2/multipredict'
        for image in list_url:
            payload = {
                # Add your client key
                'client_key': "ed5b9d7a2443b644aae60700456350238c1591bebb5bf122d7c4ade7ca78f76a",
                'model_id': list_models,
                # Add the image URL you want to process
                'image_url': image
            }

            # Make the API request
            response = requests.get(url, params=payload)


        # The response is formatted in JSON
        json_response = response.json()
        print(json_response)
        old_house = {"square_meters" : sq_meters, "bedrooms" : num_hab, "bathrooms" : num_baños, "num_images" : num_images}
        extract_image_data(json_response, old_house)
        
        if property_type == "Condo":
            old_house["property_type_numeric"] = 0
        else:
            old_house["property_type_numeric"] = 1

        old_house = pd.DataFrame.from_dict(old_house, orient="index") 
        old_house = old_house.T
        print(old_house)
        pd.set_option("display.max_rows", 180)

        #  #  predir el preu
        model = joblib.load("Completed_model.joblib")
        price_old_house = model.predict(old_house) # predicció preu de la casa amb el model
        st.write("El precio estimado de la propiedad es  aproximadamente " + str(int(price_old_house[0])) + "€." )
    #  #  veure features que falten a la casa i podrien millorar-la 
        
        not_in_house = comparison(old_house)



        with st.form("aplicar_reformas"):
            change = st.checkbox("Calidad General de la Casa")
            changes = [change]
            for i in range(1, len(not_in_house)):
                change = st.checkbox(not_in_house[i])
                changes.append(change)
            
            if st.form_submit_button("Aplicar Reformas"):
                temp_old_house = old_house.copy()
                # canvis que s'aplicaran
                if changes[0] == 1:
                    temp_old_house["image_data.r1f6.property"] = max(old_house["image_data.r1f6.property"][0] - 1, 1)

                for i in range(1, len(changes)):
                    if changes[i] == 1:
                        temp_old_house[not_in_house[i]] = 1

                price_temp_old_house = model.predict(temp_old_house)
                st.write("El precio final estimado, una vez realizadas las reformas, es " + str(int(price_temp_old_house[0])) + "€." )
            

    else:
        print("ja no")


if __name__ == "__main__":
    main()
