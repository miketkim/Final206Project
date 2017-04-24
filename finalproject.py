#SI 206 Final Project
# Michael Kim 
# Option 2 

#Import Statements 
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~OMDB caching~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

omdb_moviedata = "omdb_data.json" #caching pattern for OMDB Data 
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	omdb_diction = json.loads(cache_contents)
except:
	omdb_diction = {}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    OMDB API ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

list_of_movie_titles = ('Batman', 'Ironman', 'Superman') #making a list of at least three movies 

movie1 = omdb_data(list_of_movie_titles[0])
movie2 = omdb_data(list_of_movie_titles[1])
movie3 = omdb_data(list_of_movie_titles[2])

list_of_movie_dictionaries = [movie1, movie2, movie3]  #Creating a list of Movie dictionaries using omdb_data function (defined above)


class Movie:
	def __init__(self, omdb_moviedata):
		self.omdb_moviedata = omdb_moviedata
		self.title = omdb_moviedata['Title']
		self.runtime = omdb_moviedata['Runtime']
		self.director = omdb_moviedata['Director']

	def get_best_actor(self):
		return self.omdb_moviedata['Actors'].split(',')[0]

	def get_number_of_languages(self):
		return len(self.omdb_moviedata['Language'].split(','))

	def get_plot(self):
		return self.omdb_moviedata['Plot']

	def get_year_of_release(self):
		return self.omdb_moviedata['Year']

	def get_movie_rating(self):
		return self.omdb_moviedata['imdbRating']

	def get_id(self):
		return self.omdb_moviedata['imdbID']

	def __str__(self):
		return "{} is directed by {} and is {}".format(self.title, self.director, self.runtime)

movie_objects=[] 			# Creating a Movie instances in a list for three movies 
for x in list_of_movie_dictionaries:
	mov_object = Movie(x)
	movie_objects.append(mov_object)


def get_movie_data(movie_lst):  #CHANGE THIS 
	movie_tuple_list = []
	for movie in movie_objects:  
		movie_id = movie.get_id()
		movie_director = movie.director
		movie_title = movie.title
		movie_imdb_rating = movie.get_movie_rating() 
		movie_lead_actor = movie.get_best_actor()
		movie_num_lang = movie.get_number_of_languages()

		movie_tup = (movie_id, movie_title, movie_director, movie_num_lang, movie_imdb_rating, movie_lead_actor)
		movie_tuple_list.append(movie_tup)

	return movie_tuple_list

movie_tuple_list = get_movie_data(movie_objects)

# pprint (movie_tuple_list)






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


movie1tweets = tweets(list_of_movie_titles[0])
movie2tweets = tweets(list_of_movie_titles[1])
movie3tweets = tweets(list_of_movie_titles[2])

movietweetlist = [movie1tweets, movie2tweets, movie3tweets]  #Making a list of tweets using the title of each movie 

# pprint (movie1tweets)


tweet_tuple_list = []
for x in movietweetlist:
	for movie in x:
		text = movie['text']	
		tweet_id = movie['id_str']
		user_id = movie['user']['id_str']
		favorites = movie['favorite_count']
		retweets = movie['retweet_count']
		if "Batman" in movie['text']:
			movie_name = "Batman"
		if "Superman" in movie['text']:
			movie_name = "Superman"
		if "Antman" in movie['text']: 
			movie_name = 'Antman'

		tweet_tuple = (tweet_id, text, user_id, favorites, retweets, movie_name)
		tweet_tuple_list.append(tweet_tuple)


# pprint (tweet_tuple_list)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Twitter Users~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


twitter_user_data = 'twitter_user_data.json'
try:
	cache_file = open(twitter_user_data, 'r')
	cache_contents = cache_file.read()
	cache_file.close()
	twitter_user_diction = json.loads(cache_contents)
except:
	twitter_user_diction = {}



def getting_twitter_user_info(movietweetsdict):
	twitter_user_tuples = []	
	for x in movietweetsdict:
		user_id = x['user']['id_str']
		screen_name = x['user']['screen_name']
		num_favs = x['user']['favourites_count']
		num_followers = x['user']['followers_count']
		location = x['user']['location']
		movie_tweets_user_tup = (user_id, screen_name, num_favs, num_followers, location)
		twitter_user_tuples.append(movie_tweets_user_tup)

		if screen_name not in twitter_user_diction:
			twitter_user_diction[screen_name] = x['user']
			cache_file = open(twitter_user_data, 'w')
			cache_file.write(json.dumps(twitter_user_diction, indent =2))
			cache_file.close()
	return twitter_user_tuples

def getting_twitter_user_mentions(movietweetsdict):
	twitter_user_list = []
	for x in movietweetsdict:
		user_mentions = x['entities']['user_mentions']
		for y in user_mentions:
			user_mentions_info = api.get_user(y['screen_name'])
			user_id = y['id_str']
			screen_name = y['screen_name']
			num_favs = user_mentions_info['favourites_count']
			num_followers = user_mentions_info['followers_count']
			location = user_mentions_info['location']
			movie_tweets_user_tup = (user_id, screen_name, num_favs, num_followers, location)
			twitter_user_list.append(movie_tweets_user_tup)

			if y["screen_name"] not in twitter_user_diction:
				twitter_user_diction[y["screen_name"]] = user_mentions
				cache_file = open(twitter_user_data, 'w')
				cache_file.write(json.dumps(twitter_user_diction, indent =2))
				cache_file.close()
	return twitter_user_list


movie1users = getting_twitter_user_info(movie1tweets)

movie1usermentions = getting_twitter_user_mentions(movie1tweets)

movie2users = getting_twitter_user_info(movie2tweets)

movie2usermentions = getting_twitter_user_mentions(movie2tweets)

movie3users = getting_twitter_user_info(movie3tweets)

movie3usermentions = getting_twitter_user_mentions(movie3tweets)


twitter_user_list = [movie1users + movie1usermentions + movie2users + movie2usermentions + movie3users + movie3usermentions]

twitter_touple_lst = []
for x in twitter_user_list:
	for y in x:
		twitter_touple_lst.append(y)





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SQL Database Loading~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('DROP TABLE IF EXISTS Movies')


tweets_table_spec = 'CREATE TABLE IF NOT EXISTS Tweets (tweet_id TEXT PRIMARY KEY, message TEXT, user_id TEXT, num_favs INTEGER, num_retweets INTEGER, movie_name TEXT)' 
cur.execute(tweets_table_spec)	

tweet_db = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'
for tweet in tweet_tuple_list:
	cur.execute(tweet_db, tweet)
conn.commit()

movies_table_spec = 'CREATE TABLE IF NOT EXISTS Movies (movie_ID TEXT PRIMARY KEY, title TEXT, director TEXT, num_languages INT, IMDB_rating TEXT, best_actor TEXT)'
cur.execute(movies_table_spec)

movie_db = "INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)"
for movie in movie_tuple_list:
	cur.execute(movie_db, movie)
conn.commit()


users_table = 'CREATE TABLE IF NOT EXISTS Users (user_ID TEXT PRIMARY KEY, user TEXT, number_favs_by_user INTEGER, number_followers INTEGER, location TEXT)'
cur.execute(users_table)

user_db = 'INSERT or IGNORE INTO Users VALUES (?, ?, ?, ?, ?)'
for user in twitter_touple_lst:
	cur.execute(user_db, user)
conn.commit()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SQL Queries~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cur.execute('SELECT user FROM Users')
screen_names = [user[0] for user in cur.fetchall()]
print (screen_names)


cur.execute("SELECT Movies.title, Users.user FROM Movies INNER JOIN Users ON Users.number_followers > 10000")
popular_followers = cur.fetchall()
print (popular_followers)

conn.close()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DATA PROCESSING TECHNIQUES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Data Processing Technique #1 



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST CASES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
source_code_data = omdb_data('Source Code')
source_code = Movie(source_code_data)
conn = sqlite3.connect('finalproject.db')
cur = conn.cursor()
cur.execute('SELECT movie_ID FROM Movies');
result = cur.fetchall()
# print (result[1][0])


class MovieTests(unittest.TestCase):
	def test_1(self):
		self.assertEqual(source_code.title, "Source Code")
	def test_2(self):
		self.assertEqual(source_code.director, "Duncan Jones")
	def test_3(self):
		self.assertIn("Jake Gyllenhaal", source_code.get_best_actor())
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




