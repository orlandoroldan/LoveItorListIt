import streamlit as st 
import pandas as pd


def homepage():
    st.set_page_config(layout="wide")

    margins_css = """
        <style>
            .appview-container .main .block-container{
                padding-left: 0rem;
                padding-right: 0rem;
                padding-top: 0rem;
            }
        </style>
    """

    st.markdown(margins_css, unsafe_allow_html=True)

    title_style = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans&display=swap');

            .centered-title {
                text-align: center;
                font-family: 'Josefin Sans', sans-serif;
            }
        </style>
    """

    # Add the CSS style to the Streamlit app
    st.markdown(title_style, unsafe_allow_html=True)

    # Display the centered title
    st.markdown("<h1 class='centered-title'>Love it &nbsp;&nbsp;&nbsp; OR &nbsp;&nbsp;&nbsp; List it</h1>", unsafe_allow_html=True)

    left_col_stype = """<style>
        .left-column {
        background-image: url("https://images.unsplash.com/photo-1572120360610-d971b9d7767c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8MTF8fHxlbnwwfHx8fA%3D%3D&w=1000&q=80");
        background-size: cover;
        background-position: center;

        height:500px;
        }
        .button-container {
            position: absolute;
            top: 80%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        </style>
    """

    righ_col_style  = """<style>

        .right-column {
        background-image: url("https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
        background-size: cover;
        background-position: center;
        height:500px;
        }
        .button-container {
            position: absolute;
            top: 80%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 20px;
            font-size:30px;
            cursor: pointer;
            color: white;   
        }
        .custom_button {
            @import url('https://fonts.googleapis.com/css2?family=Josefin+Sans&display=swap');
            font-family: 'Josefin Sans', sans-serif;
            padding: 10px 20px;
        }

        .rightbutton:hover {
            background-color: #bccaf5;
        }

        .leftbutton:hover {
            background-color: 	#bcf5e7;
        }
        </style>
    """


    col1, col2 = st.columns(2, gap="small")

    # left_image_url = "https://images.unsplash.com/photo-1572120360610-d971b9d7767c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8MTF8fHxlbnwwfHx8fA%3D%3D&w=1000&q=80"
    # right_image_url = "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

    with col1:
        st.markdown(left_col_stype, unsafe_allow_html=True)
        st.markdown("<div class='left-column'><div class='button-container'><button class='custom_button leftbutton'>Love It</button></div></div>", unsafe_allow_html=True)

            # st.markdown(bg_im1, unsafe_allow_html=True)
        # col1.image(left_image_url, use_column_width=True)

        # if col1.button("Love it"):
        #     col1.write("You clicked the Left Button!")

    with col2:
        st.markdown(righ_col_style, unsafe_allow_html=True)
        st.markdown("<div class='right-column'><div class='button-container'><button class='custom_button rightbutton'>List It</button></div></div>", unsafe_allow_html=True)



if __name__ == "__main__":
    homepage()
