import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(this_fruit_choice):
	return requests.get(f"https://fruityvice.com/api/fruit/{this_fruit_choice}").json()

try:
	fruit_choice = streamlit.text_input('What fruit would you like information about?')
	if not fruit_choice:
		streamlit.error("Please select a fruit to get information.")
	else:
		fruityvice_json = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}").json()
		streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
	streamlit.error()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("select * from fruit_load_list")
#my_cur.execute("select current_user(), current_account(), current_schema(), current_database()")
my_cur.execute("select * from fruit_load_list")
rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'Kiwi')
streamlit.text(f'Thanks for adding {add_my_fruit}')
