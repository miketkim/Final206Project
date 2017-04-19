###### INSTRUCTIONS ###### Michael Kim

# An outline for preparing your final project assignment is in this file.

# Below, throughout this file, you should put comments that explain exactly what you should do for each step of your project. You should specify variable names and processes to use. For example, "Use dictionary accumulation with the list you just created to create a dictionary called tag_counts, where the keys represent tags on flickr photos and the values represent frequency of times those tags occur in the list."

# You can use second person ("You should...") or first person ("I will...") or whatever is comfortable for you, as long as you are clear about what should be done.

# Some parts of the code should already be filled in when you turn this in:
# - At least 1 function which gets and caches data from 1 of your data sources, and an invocation of each of those functions to show that they work 
# - Tests at the end of your file that accord with those instructions (will test that you completed those instructions correctly!)
# - Code that creates a database file and tables as your project plan explains, such that your program can be run over and over again without error and without duplicate rows in your tables.
# - At least enough code to load data into 1 of your dtabase tables (this should accord with your instructions/tests)

######### END INSTRUCTIONS #########

# Put all import statements you need here.
import requests
import unittest 
import itertools 
import collections 
import tweepy 
import twitter_info 
import json 
import sqlite3
from pprint import pprint

# Begin filling in instructions....

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~OMDB API~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

omdb_moviedata = "omdb_data.json" #caching pattern for OMDB Data 
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	omdb_diction = json.loads(cache_contents)
except:
	omdb_diction = {}

def movie_title_search(title1, title2, title3): #defined a function to make a list of movie titles 
	movie_titles=[]
	movie_titles.append(title1)
	movie_titles.append(title2)
	movie_titles.append(title3)
	return movie_titles

a = movie_title_search('Batman', 'Superman', 'Antman') #calling the function to get a list of movie titles
# print (a)

def omdb_data(movie_title): #Defining a function to use OMDB API 	
	movie_data_by_title = requests.get('http://www.omdbapi.com?', params = {'t': movie_title})
	url = movie_data_by_title.text
	if movie_title in omdb_diction:
		return omdb_diction[movie_title]
	else:
		omdb_diction[movie_title] = url 
		omdb_data = url 
		cache_file = open(omdb_moviedata, 'w')
		cache_file.write(json.dumps(omdb_diction, indent=2))
		cache_file.close()
		return json.loads(omdb_data)

def list_of_movie_dictionaries(title1, title2, title3): #Defining a function to get the data the 3 dictionaries contain about specific movies into a list 
	movie_dictionaries = []
	movie_dictionaries.append(title1)
	movie_dictionaries.append(title2)
	movie_dictionaries.append(title3)
	return movie_dictionaries

movie1 = omdb_data(a[0])
movie2 = omdb_data(a[1])
movie3 = omdb_data(a[2])

b = list_of_movie_dictionaries(movie1, movie2, movie3)
# print (b)

# def list_of_movie_instances(title1, title2, title3):
# 	movie_instances=[]
# 	movie_instances.append(title1)
# 	movie_instances.append(title2)
# 	movie_instances.append(title3)
# 	return movie_instances

class Movie():
	def __init__(self, omdb_moviedata = {}):
		self.omdb_moviedata = omdb_moviedata
		self.title = self.omdb_moviedata['Title']
		self.runtime = self.omdb_moviedata['Runtime']
		self.director = self.omdb_moviedata['Director']

	# def get_Rotten_Tomatoes(self):
	# 	return omdb_moviedata['Ratings']['IMD']

	def get_list_of_actors(self):
		return self.omdb_moviedata['Actors']

	def get_number_of_languages(self):
		return self.omdb_moviedata['Language']

	def get_plot(self):
		return self.omdb_moviedata['Plot']

	def get_year_of_release(self):
		return self.omdb_moviedata['Year']

	def get_movie_rating(self):
		return self.omdb_moviedata['Rated']


Batman_data = Movie(b[0])
print (Batman_data.runtime)
# print (Batman_data.get_list_of_actors())
# print (Batman_data.get_movie_rating())
# print (Batman_data.get_plot())
# # Superman_data = Movie(b[1])
# # Antman_data = Movie(b[2])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SQL Database Part~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()


cur.execute('DROP TABLE IF EXISTS Movies')

movies_table_spec = 'CREATE TABLE IF NOT EXISTS Movies (movie_ID TEXT PRIMARY KEY, title TEXT, director TEXT, num_languages INT, IMDB_rating TEXT)'
cur.execute(movies_table_spec)

movie_database= []
for row in b:
	movie_id = row['imdbID']
	title = row['Title']
	director = row['Director']
	imdb = row['imdbRating']
	languages = row['Language']
	movie_tuple = (movie_id, title, director, languages, imdb)
	movie_database.append(movie_tuple)
print (movie_database)

movie_db= "INSERT INTO Movies VALUES (?, ?, ?, ?, ?)"
for movie in movie_database:
	cur.execute(movie_db, movie)

conn.commit()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST CASES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
source_code_data = omdb_data('Source Code')
source_code = Movie(source_code_data)
conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()
cur.execute('SELECT movie_ID FROM Movies');
result = cur.fetchall()
print (result[1][0])


class MovieTests(unittest.TestCase):
	def test_1(self):
		self.assertEqual(source_code.title, "Source Code")
	def test_2(self):
		self.assertEqual(source_code.director, "Duncan Jones")
	def test_3(self):
		self.assertIn("Jake Gyllenhaal", source_code.get_list_of_actors())
	def test_4(self):
		self.assertEqual(source_code.get_year_of_release(), "2011")
class DBTests(unittest.TestCase):
	def test_5(self):
		conn = sqlite3.connect('finalproject.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[0]), 5)
		conn.close()
	# def test_6(self):
	# 	conn = sqlite3.connect('finalproject.db')
	# 	cur = conn.cursor()
	# 	cur.execute('SELECT movie_ID FROM Movies');
	# 	result = cur.fetchall()
	# 	self.assertTrue(result[1][0])= 3))
	# def test_7(self):
	# 	conn = sqlite3.connect('finalproject.db')
	# 	cur = conn.cursor()
	# 	cur.execute('SELECT * FROM Movies');
	# 	result = cur.fetchall()
	# 	self.assertEqual(len(result[0]), 6)	
	# def test_8(self):
	# 	conn = sqlite3.connect('finalproject.db')
	# 	cur = conn.cursor()
	# 	cur.execute('SELECT * FROM Users'); 
	# 	result = cur.fetchall()
	# 	self.assertEqual(len(resutl[0]), 3)
# ## Remember to invoke all your tests...
if __name__ == "__main__":
    unittest.main(verbosity=2)




