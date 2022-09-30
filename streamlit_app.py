import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')

streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach, and Arugula Smoothie')
streamlit.text('Hard-boiled Free-Range Egg')
streamlit.text('🥑\N{bread}Avocado Toast')

streamlit.header('Build your own Fruit Smoothie')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", 
						list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')

fc = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
r = requests.get(f"https://fruityvice.com/api/fruit/{fc}").json()
streamlit.dataframe(pandas.json_normalize(r))

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select current_user(), current_account(), current_region()")
row = my_cur.fetchone()
streamlit.text("Hello from snowflake")
streamlit.text(row)