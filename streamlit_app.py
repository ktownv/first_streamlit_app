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


streamlit.header("The fruit load list contains:")

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

def get_fruit_load_list():
	with my_cnx.cursor() as my_cur:
		my_cur.execute("select * from fruit_load_list")
		return my_cur.fetchall()


if streamlit.button('Get Fruit Load List:'):
	streamlit.dataframe(get_fruit_load_list())

def insert_row_snowflake(new_fruit):
	with my_cnx.cursor() as my_cur:
		my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
		return f'thanks for adding {new_fruit}'



add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to list'):
	streamlit.text(insert_row_snowflake(add_my_fruit))
