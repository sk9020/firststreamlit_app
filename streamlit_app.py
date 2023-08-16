import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Sugreev Snowflake Badge 2 course')
streamlit.header('Learning app building with streamlit')
streamlit.text('Badge 2')

streamlit.title('Food')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show =  my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# function to get fruityvice data
function get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       return fruityvice_normalized

# New section to display fruityVice api
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.errror("Please select a fruit to get information")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
       # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
       #  # streamlit.text(fruityvice_response.json())
       # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       # streamlit.dataframe(fruityvice_normalized)
   
except URLError as e:
 streamlit.error()

streamlit.stop()
# import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("Fruit load list contains:")
streamlit.dataframe(my_data_row)
fruit_choice_from_fruit_list = streamlit.text_input('What fruit would you like to add','Jackfruit')
streamlit.text("Thanks for adding " + fruit_choice_from_fruit_list)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")

