import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('NGSS New Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boilded Free Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", 
                                        list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# Display the table on the page.
streamlit.header('Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    streamlit.dataframe(get_fruityvice(fruit_choice))

except URLError as e:
    streamlit.error()

streamlit.write('The fruit load list contains:')

# Snowflake-related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  streamlit.dataframe(my_data_row)

# Allow the end user to add a fruit to the list
# Snowflake-related functions
def insert_row_in_SF(new_fruit):
   with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")
        return "Thanks for adding : " + new_fruit
   
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit To The List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.text(insert_row_in_SF(add_my_fruit))

