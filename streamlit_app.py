import streamlit as st
import snowflake.connector
import pandas as pd

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
    ingredients_string = ' '.join(ingredients_list) + ' '

    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        cur.execute(my_insert_stmt)
        conn.commit()
        st.success('Your Smoothie is ordered!', icon="✅")
import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response)
