import streamlit as st
import snowflake.connector
import pandas as pd
import requests  
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name On Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

conn = snowflake.connector.connect(
    account=st.secrets["connections"]["snowflake"]["account"],
    user=st.secrets["connections"]["snowflake"]["user"],
    password=st.secrets["connections"]["snowflake"]["password"],
    warehouse=st.secrets["connections"]["snowflake"]["warehouse"],
    database=st.secrets["connections"]["snowflake"]["database"],
    schema=st.secrets["connections"]["snowflake"]["schema"],
    role=st.secrets["connections"]["snowflake"]["role"]
)

cur = conn.cursor()
cur.execute("SELECT FRUIT_NAME FROM smoothies.public.fruit_options")
my_dataframe = pd.DataFrame(cur.fetchall(), columns=["FRUIT_NAME"])

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe["FRUIT_NAME"].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)  
        sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)
    
