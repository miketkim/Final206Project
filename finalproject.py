import requests
import unittest 
import itertools 
import collections 
import tweepy 
import twitter_info 
import json 
import sqlite3
from pprint import pprint

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

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

a = movie_title_search(input("Enter a movie title: "), input('Enter another movie title: '), input('Enter a 3rd movie title: ')) #calling the function to get a list of movie titles
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

batman = omdb_data('Batman')
superman = omdb_data('Superman')
antman = omdb_data('Antman')

b = list_of_movie_dictionaries(batman, superman, antman)
# print (b)

def list_of_movie_instances(title1, title2, title3):
	movie_instances=[]
	movie_instances.append(title1)
	movie_instances.append(title2)
	movie_instances.append(title3)
	return movie_instances

class Movie:
	def __init__(self, omdb_moviedata = {}):
		self.omdb_moviedata = omdb_moviedata
		if "Title" in omdb_moviedata:
			self.title = self.omdb_moviedata['Title']
		if "Runtime" in omdb_moviedata:
			self.runtime = self.omdb_moviedata['Runtime']
		if 'Director' in omdb_moviedata:
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
# print (Batman_data.get_list_of_actors())
# print (Batman_data.get_movie_rating())
# print (Batman_data.get_plot())
# # Superman_data = Movie(b[1])
# # Antman_data = Movie(b[2])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Tweets~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

twitter_data = "twitter_data.json"
try:
	cache_file = open(twitter_data, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	twitter_diction = json.loads(cache_contents)
except:
	twitter_diction = {}


def tweets(search):
	if search in twitter_diction:
		tweets = twitter_diction[search]
	else:
		tweets = api.search(q = search) 
		twitter_diction[search] = tweets		
		cache = open(twitter_data,'w')
		cache.write(json.dumps(twitter_diction, indent=2))
		cache.close()
	return tweets['statuses']


movie1tweets = tweets(a[0])
movie2tweets = tweets(a[1])
movie3tweets = tweets(a[2])


def tweet_tuple(tweet_list):
	for movie in tweet_list:
		if 'text' in movie: 
			text = movie['text']
		if 'id_str' in movie: 
			tweet_id = movie['id_str']
		if "user" in movie:
			user_id = movie['user']['id_str']
		if 'favorite_count' in movie: 
			favorites = movie['favorite_count']
		if 'retweet_count' in movie: 
			retweets = movie['retweet_count']
	tweet_tuple = (tweet_id, text, user_id, favorites, retweets)
	return tweet_tuple

tweet_tuple_list = [tweet_tuple(movie1tweets), tweet_tuple(movie2tweets), tweet_tuple(movie3tweets)]

print (tweet_tuple_list)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Twitter Users~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


twitter_user_data = 'twitter_user_data'
try:
	cache_file = open(twitter_user_data, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	twitter_user_diction = json.loads(cache_contents)
except:
	twitter_user_diction = {}



# def twitteruserdata(handle):
# 	if handle in twitter_user_diction:
# 		user = twitter_user_diction[handle]
# 	else:
# 		user = api.


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SQL Database Part~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('DROP TABLE IF EXISTS Movies')


tweets_table_spec ='CREATE TABLE IF NOT EXISTS Tweets (tweet_id TEXT PRIMARY KEY, message TEXT, user_id TEXT, num_favs INTEGER, num_retweets INTEGER)' 
cur.execute(tweets_table_spec)	

tweet_db = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'
for tweet in tweet_tuple_list:
	cur.execute(tweet_db, tweet)
conn.commit()

movies_table_spec = 'CREATE TABLE IF NOT EXISTS Movies (movie_ID TEXT PRIMARY KEY, title TEXT, director TEXT, num_languages INT, IMDB_rating TEXT)'
cur.execute(movies_table_spec)
conn.commit()

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

movie_db = "INSERT INTO Movies VALUES (?, ?, ?, ?, ?)"
for movie in movie_database:
	cur.execute(movie_db, movie)
conn.commit()

# users_table_spec = 'CREATE TABLE IF NOT EXISTS'
# users_table_spec += 'Users (users_ids TEXT PRIMARY KEY, users TEXT, number_favs_by_user INTEGER'
# cur.excute(users_table_spec)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST CASES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MovieTests(unittest.TestCase):
	def test_1(self):
		source_code_data = omdb_data('Source Code')
		source_code = Movie(source_code_data)
		self.assertEqual(source_code.title, "Source Code")
	def test_2(self):
		source_code_data = omdb_data('Source Code')
		source_code = Movie(source_code_data)
		self.assertEqual(source_code.director, "Duncan Jones")
	def test_3(self):
		source_code_data = omdb_data('Source Code')
		source_code = Movie(source_code_data)
		self.assertIn(source_code.get_list_of_actors(), "Jake Gyllenhaal")
	def test_4(self):
		source_code = Movie(source_code_data)
		self.assertEqual(source_code_length.extremely_long_movie(), "This movie is less than 2 hours.  Enjoy!")
# class DBTests(unittest.TestCase):
# 	def test_5(self):
# 		conn = sqlite3.connect('finalproject.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Tweets');
# 		result = cur.fetchall()
# 		self.assertTrue(len(result)>=20)
# 		conn.close()
# 	def test_6(self):
# 		conn = sqlite3.connect('finalproject.db')
# 		cur = conn.cursor()
# 		cur.excute('SELECT * FROM Tweets'); 
# 		result = cur.fetchall()
# 		self.assertEqual(len(result[0]), 6)
# 		conn.close()
# 	def test_7(self):
# 		conn = sqlite3.connect('finalproject.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Movies');
# 		result = cur.fetchall()
# 		self.assertEqual(len(result[0]), 6)	
# 	def test_8(self):
# 		conn = sqlite3.connect('finalproject.db')
# 		cur = conn.cursor()
# 		cur.execute('SELECT * FROM Users'); 
# 		result = cur.fetchall()
# 		self.assertEqual(len(resutl[0]), 3)
# ## Remember to invoke all your tests...
if __name__ == "__main__":
    unittest.main(verbosity=2)




